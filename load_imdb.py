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

            if int(row['runtimeMinutes']) < 60:
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
        films[film["id"]]= film
        # test_count += 1
        # if test_count == 1000:
        #     break

with open("title.ratings.tsv", 'r') as ratings:
    reader = csv.DictReader(ratings, delimiter='\t')
    for row in reader:
        filmId = row['tconst']
        if filmId in films:
            if int(row['numVotes']) < 8000 or float(row['averageRating']) < 7.0:
                films.pop(filmId)

print(len(films))

with open("title.principals.tsv", 'r') as principals:
    reader = csv.DictReader(principals, delimiter='\t')
    for row in reader:
        filmId = row['tconst']
        if filmId in films:
            films[filmId].setdefault('principals', []).append(row['nconst'])

with open("name.basics.tsv", 'r') as names:
    with open("name.short.tsv", 'w') as names_out:
        names_out.write("id\tname")
        reader = csv.DictReader(names, delimiter='\t')
        for row in reader:
            knownFors = row['knownForTitles'].split(',')
            for knownFor in knownFors:
                if knownFor in films:
                    # films[knownFor].setdefault('principals', []).append({'id': row['nconst'], 'name': row['primaryName']})
                    names_out.write(f"\n{row['nconst']}\t{row['primaryName']}")
                    break

with open('combined.tsv', 'w', newline='') as tsvfile:
    fieldnames = list(films.values())[0].keys()
    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')

    writer.writeheader()
    for id in films:
        films[id]["principals"] = ",".join(films[id]["principals"])
        writer.writerow(films[id])

