import pandas as pd
import config
from time import time
from glob import glob

# Cargo archivo SQL con scores
cons = pd.read_csv(config.DATA_EXTERNAL + "phastConsElements46wayPrimates.csv")

#dataset = pd.read_csv("../data/processed/humsavar_gt.tab.gz", sep="\t", 
#    usecols["MUTANT"]).squeeze().str.split("-").apply(lambda x: x[0])

 
for chrom in cons.chrom.unique():
    timeInit = time()
    print("Chromosome: {}".format(chrom))
    cons_filtered = cons[cons.chrom == chrom]
    
    hum_clean = pd.read_csv(config.DATA_INTERIM + "humsavar_clean_201711.csv.gz", chunksize=2500)
    res = []
    for e, chunk in enumerate(hum_clean):
        print("Chunk: ", e)
        #chunk = chunk[chunk["Swiss Prot AC"].isin(dataset)]
        chunk = chunk[~chunk.dbSNP.isnull()]
        chunk = chunk[["dbSNP"]].drop_duplicates()
        dbsnp = pd.read_csv(config.DATA_EXTERNAL + "dbsnp.csv.gz")
        chunk = chunk.merge(dbsnp, right_on="name", left_on="dbSNP", how="left")
        #chunk = chunk[(chunk.chromEnd - chunk.chromStart == 1)]
        chunk_filtered = chunk[chunk.chrom == chrom]
        merging_chrom = cons_filtered.merge(chunk_filtered, on="chrom")
        merging_chrom = merging_chrom[(merging_chrom.chromStart_y >= merging_chrom.chromStart_x) &
                                     (merging_chrom.chromEnd_y <= merging_chrom.chromEnd_x)]
        res.append(merging_chrom)
    pd.concat(res).to_csv(config.DATA_INTERIM + "chrom/{}.csv".format(chrom), index=False)
    timeEnd = time()
    print("Time elapsed: {}s".format(timeEnd - timeInit))
    
    
res = []
for f in glob(config.DATA_INTERIM + "chrom/*"):
    print(f)
    df = pd.read_csv(f)
    res.append(df)
    
res = pd.concat(res)
res = res[["dbSNP", "score"]].rename(columns={"score": "CONS46WAY"})
res.to_csv(config.DATA_INTERIM + "cons46way.csv", index=False)
