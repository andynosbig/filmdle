import csv
import random

filmsByTitle = {}
with open("combined.tsv", 'r') as basics:
    reader = csv.DictReader(basics, delimiter='\t')
    for row in reader:
        filmsByTitle[row['title']] = row
        filmsByTitle[row['title']].pop('id')
        
        filmsByTitle[row['title']]['genres'] = row['genres'].split(',')
        filmsByTitle[row['title']]['principals'] = row['principals'].split(',')
        filmsByTitle[row['title']].pop('title')

print(filmsByTitle)

