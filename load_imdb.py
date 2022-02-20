import csv
import pprint

films = {}
all_genres = set()
test_count = 0
with open("title.basics.tsv", 'r') as basics:
    reader = csv.DictReader(basics, delimiter='\t')
    for row in reader:
        if row['titleType'] != 'movie':
            continue
        if row['isAdult'] != '0':
            continue
        try:
            if int(row['startYear']) < 1980:
                continue

            if int(row['runtimeMinutes']) < 80:
                continue
        except:
            continue
        
        if '\\N' in row['genres']:
            continue
        if 'Documentary' in row['genres']:
            continue
        if 'Reality-TV' in row['genres']:
            continue
        if 'Adult' in row['genres']:
            continue

        film = {}
        film["id"] = row['tconst']
        film["title"] = row['primaryTitle']
        film["startYear"] = int(row['startYear'])
        film["genres"] = row['genres']
        film.setdefault('principals', [])
        films[film["id"]]= film

print("post genres, length, year filtering", len(films))

rated_films = {}
with open("title.ratings.tsv", 'r') as ratings:
    reader = csv.DictReader(ratings, delimiter='\t')
    for row in reader:
        filmId = row['tconst']
        if filmId in films:
            if int(row['numVotes']) > 10000 and float(row['averageRating']) > 6.5:
                rated_films[filmId] = films[filmId]

print("post popularity filtering", len(rated_films))
films = rated_films
film_names = {}


def read_rows_until_crash(reader, film_names):
    try:
        # hopefully starts where it left off
        for row in reader:
            if row['titleId'] in films:
                if row['isOriginalTitle']:
                    film_names.setdefault(row['titleId'], {})["original"] = row['title']
                if row['region'] == "US":
                    film_names.setdefault(row['titleId'], {})["US"] = row['title']
                if row['region'] == "GB":
                    film_names.setdefault(row['titleId'], {})["GB"] = row['title']
    except:
        return 1
    # actually finished
    return 0

with open("title.akas.tsv", 'r') as titles:
    reader = csv.DictReader(titles, delimiter='\t')
    # possibly some unicode issue causes a "too many column error" somewhere in this file, try to get past by swallowing exception
    while read_rows_until_crash(reader, film_names):
        continue

for id in film_names:
    if (film_names[id].get("original") != film_names[id].get("US")) or (film_names[id].get("original") != film_names[id].get("GB")):
        films.pop(id)

print("post language filtering", len(films))

all_principals = set()
with open("title.principals.tsv", 'r') as principals:
    reader = csv.DictReader(principals, delimiter='\t')
    for row in reader:
        filmId = row['tconst']
        if filmId in films and row['category'] in ["actor", "actress", "director"]:
            films[filmId].setdefault('principals', []).append(row['nconst'])
            all_principals.add(row['nconst'])

principal_names = {}
with open("name.basics.tsv", 'r') as names:
    reader = csv.DictReader(names, delimiter='\t')
    for row in reader:
        if row['nconst'] in all_principals:
            principal_names[row['nconst']] = row['primaryName']

with open('principals.tsv', 'w', newline='') as tsvfile:
    writer = csv.DictWriter(tsvfile, fieldnames=["id", "name"], delimiter='\t')

    writer.writeheader()
    for id in principal_names:
        writer.writerow({"id": id, "name": principal_names[id]})

with open('combined.tsv', 'w', newline='') as tsvfile:
    fieldnames = list(films.values())[0].keys()
    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')

    writer.writeheader()
    for id in films:
        films[id]["principals"] = ",".join(films[id]["principals"])
        writer.writerow(films[id])


