# import tarfile
# import subprocess
# import shutil
# datasets = ["https://datasets.imdbws.com/name.basics.tsv.gz",
#             "https://datasets.imdbws.com/title.akas.tsv.gz",
#             "https://datasets.imdbws.com/title.basics.tsv.gz",
#             "https://datasets.imdbws.com/title.principals.tsv.gz",
#             "https://datasets.imdbws.com/title.ratings.tsv.gz"]

# for ds in datasets:
#     outpath = f"./imdb_data/{ds.split('/')[-1]}"
#     subprocess.run(["wget", "--no-check-certificate", ds, "-O", outpath])
#     with tarfile.open(outpath, "r:gz") as t:
#         t.extractall()
