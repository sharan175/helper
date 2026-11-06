import sys
current_key = None
running_sum = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split('\t')
    if len(parts) != 3: continue
    user, feat, val = parts
    key = user + "\t" + feat
    if current_key is not None and key != current_key:
        print("%s\t%f" % (current_key, running_sum))
        running_sum = 0.0
    current_key = key
    try:
        running_sum += float(val)
    except:
        pass
if current_key is not None:
    print("%s\t%f" % (current_key, running_sum))
