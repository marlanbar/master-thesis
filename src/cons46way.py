import pandas as pd
from time import time
from glob import glob

DATA_EXTERNAL = "../data/external/"
DATA_PROCESSED = "../data/processed/"
DATA_INTERIM = "../data/interim/"

cons = pd.read_csv(DATA_EXTERNAL + "phastConsElements46wayPrimates.csv")

dataset = pd.read_csv("../data/processed/humsavar_protparam_gt.tab.gz", sep="\t", 
    usecols["MUTANT"]).squeeze().str.split("-").apply(lambda x: x[0])

hum_clean = pd.read_csv(DATA_INTERIM + "humsavar_clean_201711.csv.gz")
hum_clean = hum_clean[hum_clean["Swiss Prot AC"].isin(dataset)]
hum_clean = hum_clean[~hum_clean.dbSNP.isnull()]
hum_clean = hum_clean[["dbSNP"]]

dbsnp = pd.read_csv(DATA_EXTERNAL + "dbsnp.csv.gz")

hum_clean = hum_clean.merge(dbsnp, right_on="name", left_on="dbSNP", how="left")
#hum_clean = hum_clean[(hum_clean.chromEnd - hum_clean.chromStart == 1)]

for chrom in hum_clean.chrom.unique():
    timeInit = time()
    print("Chromosome: {}".format(chrom))
    cons_filtered = cons[cons.chrom == chrom]
    hum_clean_filtered = hum_clean[hum_clean.chrom == chrom]
    merging_chrom = cons_filtered.merge(hum_clean_filtered, on="chrom")
    merging_chrom = merging_chrom[(merging_chrom.chromStart_y >= merging_chrom.chromStart_x) &
                                 (merging_chrom.chromEnd_y <= merging_chrom.chromEnd_x)]
    merging_chrom.to_csv(DATA_INTERIM + "chrom/{}.csv".format(chrom), index=False)
    timeEnd = time()
    print("Time elapsed: {}s".format(timeEnd - timeInit))
    
    
res = []
for f in glob(DATA_INTERIM + "chrom/*"):
    df = pd.read_csv(f)
    res.append(df)
res = pd.concat(res)
res = res[["dbSNP", "score"]].rename(columns={"score": "CONS46WAY"}, inplace=True)
res.to_csv(DATA_INTERIM + "cons46way.csv", index=False)