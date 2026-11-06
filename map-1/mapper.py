import sys
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split()
    a, b, val = parts
    if a.startswith('U'):
        print("%s\tR\t%s\t%s" % (b, a, val))
    elif a.startswith('I'):
        print("%s\tF\t%s\t%s" % (a, b, val))
