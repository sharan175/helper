import sys
current_item = None
user_ratings = []
feat_values = []

def flush_products():
    for user, rating in user_ratings:
        for feat, value in feat_values:
            product = float(rating) * float(value)
            print("%s\t%s\t%s" % (user, feat, product))

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split('\t')
    if len(parts) != 4: continue
    item, tag, x, y = parts
    if current_item is not None and item != current_item:
        flush_products()
        user_ratings = []
        feat_values = []
    current_item = item
    if tag == 'R':
        user_ratings.append((x, y))
    elif tag == 'F':
        feat_values.append((x, y))

if current_item is not None:
    flush_products()
