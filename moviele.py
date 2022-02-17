import csv
import random
actorsById = {}
with open("name.short.tsv", 'r') as actors:
    reader = csv.DictReader(actors, delimiter='\t')
    for row in reader:
        actorsById[row['id']] = row['name']

filmsByTitle = {}
with open("combined.tsv", 'r') as basics:
    reader = csv.DictReader(basics, delimiter='\t')
    for row in reader:
        filmsByTitle[row['title']] = row
        filmsByTitle[row['title']]['genres'] = row['genres'].split(',')
        filmsByTitle[row['title']]['principals'] = row['principals'].split(',')



print(actorsById)

