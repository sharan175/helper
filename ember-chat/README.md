# Ember

An original, local-first character-chat web app: a little spark, a whole new story.

## Run

Python **3.10+** is required. No Node.js or frontend build step.

```bash
cd /workspace/ember-chat
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open **http://localhost:8765**. The server binds to `0.0.0.0:8765` as requested. If running on another computer, use that computer's reachable address and port. The first visit asks you to confirm you are 18+.

1. Open **Settings**, choose xAI, OpenAI, Groq, or Custom, and paste **your own API key**.
2. Keep or edit the model name. Validate & save checks fields only; it makes no billable test call.
3. Discover a character, open their profile, and start a conversation. Without a key you can explore the interface, create characters, and read greetings, but generated replies require a working key and available provider quota.

Default models: xAI `grok-4-fast` (automatically retries `grok-2-latest` on a 404), OpenAI `gpt-4o-mini`, Groq `llama-3.3-70b-versatile`. Model availability changes; edit the model if your account requires another name. Custom requires a public HTTPS OpenAI-compatible base URL (for example `https://provider.example/v1`, without `/chat/completions`). Private and local-network custom endpoints are blocked.

## Included

- Eight original illustrated adult characters, individual SVG portraits, profiles, and interests. Every character is NSFW-eligible.
- Discover search, interest filtering, intentional empty states.
- Character creation, editing, deletion, initials fallback, image URL or resized image upload.
- Streaming chat with stop button, Enter to send, Shift+Enter newline, provider errors and retry.
- Saved conversations, resuming and deletion; human display name and persona.
- Responsive dark charcoal, amber and rose interface; keyboard-friendly controls and reduced-motion support.
- Python FastAPI proxy handles provider CORS. It requests SSE, accepts full JSON responses, and retries without streaming when a compatible provider explicitly rejects the stream option.

## Storage, privacy, and safety

**API keys, settings, custom characters and conversations are saved in this browser's localStorage. Keys are not encrypted at rest.** Use a trusted device/browser profile; anyone with access to that browser origin can potentially read them. Settings provides a Forget API key button. Browser site-data clearing removes everything. There is no account, cloud sync, telemetry, server-side conversation database, or key logging. Uploaded avatars become resized WebP data URLs stored locally; remote image URLs are fetched by your browser. Google Fonts are an optional external stylesheet dependency; system fonts work offline.

The key is sent in the `X-API-Key` header to this app's proxy for the duration of each request. The server forwards it only to the chosen provider, never persists it, and does not return raw provider errors that might contain sensitive data. Chat history (most recent 60 messages), character details, and persona are sent to that provider. Normal provider API charges and policies apply. A Custom endpoint receives the supplied key: only configure endpoints you trust.

All seed characters are 21+. The UI and backend reject character ages below 21. Every system prompt requires staying in character as an adult 21+, never portraying or involving anyone under 21, and refusing requests involving minors. There are no SFW, Suggestive, or Mature content ratings; every character is NSFW-eligible for any adult fictional content the user asks for. An 18+ confirmation is self-attestation, not identity verification. Prompt instructions are not a replacement for provider-side moderation or a production safety system.

**Local personal-use prototype, not a hardened public service.** No authentication, per-user server accounts, or rate limiting. Because the requested bind is `0.0.0.0`, do not expose it to an untrusted network. Restrict access with a firewall. For public use, add authentication, HTTPS, request-size/rate controls and appropriate moderation. Custom URL DNS checks reject non-public addresses, but are not a complete defense against malicious DNS rebinding; do not run an open public proxy.

Ember is an independently made, fan-made style character-chat app, **not affiliated with SpicyChat**. Its name, branding, artwork, and characters are original; no third-party fictional characters are included.

## Files

```text
app.py                   FastAPI proxy + static hosting
requirements.txt         Python dependencies
static/index.html        App shell + age gate
static/styles.css        Responsive theme
static/app.js            Vanilla frontend + local persistence
static/seeds.js          Embedded first-load character data
static/avatars/*.svg     Eight original SVG portrait illustrations
static/favicon.svg       Original ember mark
 data/characters.json    Seed data, also exposed at GET /api/characters
 data/build_seeds.py     Optional seed/portrait regeneration helper
```

## Smoke checks

```bash
curl -i http://127.0.0.1:8765/
curl -i -X POST http://127.0.0.1:8765/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"provider":"openai","messages":[{"role":"user","content":"Hello"}],"character":{"name":"Test adult","age":28}}'
```

The second request returns a readable 400 error about the missing API key, without contacting a provider. Invalid character ages return 422. Real provider success requires your key; none is bundled.
