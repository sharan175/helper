import sys
import csv
# Read each line from tags.csv
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("userId"):  # skip header
        continue
    try:
        # Parse CSV line safely
        fields = next(csv.reader([line]))
        movieId = fields[1]   # 2nd column = movieId
        tag = fields[2]       # 3rd column = tag
        if movieId and tag:
            # Emit key=movieId, value=tag
            print("%s\t%s" % (movieId, tag))
    except Exception:
        continue
