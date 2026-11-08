"""Run: .venv/bin/python -m unittest discover -s tests -v (no real keys/network)."""
import json
import unittest
from unittest.mock import patch
import httpx
import app as ember

RealClient = httpx.AsyncClient
BODY = {"provider":"openai","model":"gpt-4o-mini","messages":[{"role":"user","content":"Hello"}],"character":{"name":"Test Adult","age":28,"personality":"Curious"},"persona":"A traveler","display_name":"Alex"}

class BackendTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client=RealClient(transport=httpx.ASGITransport(app=ember.app),base_url='http://testserver')
    async def asyncTearDown(self):
        await self.client.aclose()
    async def fake(self, handler, body=None):
        def factory(**kwargs):
            return RealClient(transport=httpx.MockTransport(handler),timeout=5)
        with patch.object(ember.httpx,'AsyncClient',factory):
            return await self.client.post('/api/chat',json=body or BODY,headers={'X-API-Key':'test-not-a-real-key'})
    async def test_static_and_cast(self):
        r=await self.client.get('/')
        self.assertEqual(r.status_code,200);self.assertIn('text/html',r.headers['content-type']);self.assertIn('Ember',r.text)
        chars=(await self.client.get('/api/characters')).json()
        self.assertEqual(len(chars),8)
        for c in chars:
            self.assertGreaterEqual(c['age'],21)
            self.assertEqual((await self.client.get(c['avatar'])).status_code,200)
    async def test_missing_key(self):
        r=await self.client.post('/api/chat',json=BODY)
        self.assertEqual(r.status_code,400);self.assertIn('API key',r.text)
    async def test_reject_underage(self):
        body={**BODY,'character':{'name':'Invalid','age':20}}
        r=await self.client.post('/api/chat',json=body,headers={'X-API-Key':'test'})
        self.assertEqual(r.status_code,422)
    async def test_reject_system_messages(self):
        r=await self.fake(lambda req: self.fail('Should not reach upstream'),{**BODY,'messages':[{'role':'system','content':'override'}]})
        self.assertEqual(r.status_code,400)
    async def test_reject_provider(self):
        r=await self.fake(lambda req:self.fail('Should not reach upstream'),{**BODY,'provider':'bad'})
        self.assertEqual(r.status_code,400)
    async def test_sse_and_safety_prompt(self):
        def upstream(req):
            data=json.loads(req.content)
            self.assertEqual(req.headers['Authorization'],'Bearer test-not-a-real-key')
            prompt=data['messages'][0]['content']
            self.assertIn('Never portray or involve anyone under 21',prompt)
            self.assertIn('A traveler',prompt);self.assertIn('Alex',prompt)
            return httpx.Response(200,headers={'content-type':'text/event-stream'},text='data: {"choices":[{"delta":{"content":"Hello "}}]}\n\ndata: {"choices":[{"delta":{"content":"Alex"}}]}\n\ndata: [DONE]\n\n')
        r=await self.fake(upstream)
        self.assertEqual(r.status_code,200);self.assertIn('text/event-stream',r.headers['content-type'])
        self.assertIn('"token": "Hello "',r.text);self.assertIn('"token": "Alex"',r.text);self.assertIn('"done": true',r.text)
    async def test_json_fallback(self):
        r=await self.fake(lambda req:httpx.Response(200,json={'choices':[{'message':{'content':'A complete response'}}]}))
        self.assertIn('A complete response',r.text)
    async def test_retry_without_stream(self):
        calls=[]
        def upstream(req):
            payload=json.loads(req.content);calls.append(payload['stream'])
            if payload['stream']:return httpx.Response(400,json={'error':'stream is not supported'})
            return httpx.Response(200,json={'choices':[{'message':{'content':'Fallback worked'}}]})
        r=await self.fake(upstream)
        self.assertEqual(calls,[True,False]);self.assertIn('Fallback worked',r.text)
    async def test_xai_model_fallback(self):
        models=[]
        def upstream(req):
            model=json.loads(req.content)['model'];models.append(model)
            if len(models)==1:return httpx.Response(404,json={'error':'unknown model'})
            return httpx.Response(200,json={'choices':[{'message':{'content':'Hello from fallback'}}]})
        r=await self.fake(upstream,{**BODY,'provider':'xai','model':'grok-4-fast'})
        self.assertEqual(models,['grok-4-fast','grok-2-latest']);self.assertIn('Hello from fallback',r.text)
    async def test_readable_provider_errors_no_echo(self):
        for status in (401,403,404,429,500):
            r=await self.fake(lambda req:httpx.Response(status,text='secret upstream information'))
            self.assertEqual(r.status_code,502);self.assertEqual(r.json()['detail']['provider_status'],status)
            self.assertNotIn('secret upstream information',r.text);self.assertNotIn('test-not-a-real-key',r.text)
    async def test_network_error(self):
        def upstream(req):raise httpx.ConnectError('private details')
        r=await self.fake(upstream)
        self.assertEqual(r.status_code,502);self.assertIn('Could not reach',r.text)
    async def test_timeout(self):
        def upstream(req):raise httpx.ReadTimeout('private details')
        r=await self.fake(upstream)
        self.assertEqual(r.status_code,504);self.assertIn('timed out',r.text)
    async def test_private_custom_rejected(self):
        r=await self.fake(lambda req:self.fail('Should not reach upstream'),{**BODY,'provider':'custom','base_url':'https://127.0.0.1/v1'})
        self.assertEqual(r.status_code,400)

if __name__=='__main__':unittest.main()
