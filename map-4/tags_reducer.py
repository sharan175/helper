import sys
import csv
# Load movies.csv into dictionary (movieId -> title)
movies = {}
with open("movies.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        movies[row[0]] = row[1]
current_movie = None
tags = []
# Read mapper output
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    movieId, tag = line.split("\t", 1)
    if current_movie == movieId:
        tags.append(tag)
    else:
        if current_movie:
            title = movies.get(current_movie, current_movie)
            print("%s\t%s" % (title, ",".join(tags)))
        current_movie = movieId
        tags = [tag]
# Print last movie
if current_movie:
    title = movies.get(current_movie, current_movie)
    print("%s\t%s" % (title, ",".join(tags)))
