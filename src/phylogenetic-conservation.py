# coding: utf-8
from __future__ import print_function
import pandas as pd
import numpy as np
import sys
from glob import glob
from time import time

var = sys.argv[1]

DATA_INTERIM = "../data/interim/"
DATA_EXTERNAL = "../data/external/"
DATA_PROCESSED = "../data/processed/"

dbsnp = pd.read_csv("../data/external/dbsnp.csv.gz")
#humsavar_dbsnp = pd.read_csv("../data/processed/humsavar_gt_dbSNP.txt")
#dbsnp = dbsnp[dbsnp.name.isin(humsavar_dbsnp.dbSNP)]
dbsnp["dist"] = dbsnp.chromEnd - dbsnp.chromStart
dbsnp_dist1 = dbsnp[dbsnp.dist == 1]

res = []
for e, chrom in enumerate(dbsnp_dist1.chrom.unique()):
    print("Chrom: ", chrom)
    timeInit = time()
    dbsnp_filtered = dbsnp_dist1[dbsnp_dist1.chrom == chrom].set_index("chromStart")
    try:
        score_table = pd.read_csv(DATA_INTERIM + "parsed_" + var + "/" + chrom + "." + var + ".csv.gz",
                header=None, names=["chr", "chromStart", var], usecols=["chromStart", var], dtype={"chromStart": np.int64}, index_col="chromStart")
        score_table = score_table[score_table.index.isin(dbsnp_filtered.index)]
        res.append(score_table.join(dbsnp_filtered)[[var]])
    except Exception as e:
        print("Exception: ", e)
        continue
    timeEnd = time()
    print("Time Elapsed: {:.2f}s.".format(timeEnd - timeInit))
res = pd.concat(res)
res.to_csv(DATA_PROCESSED + var + ".csv", index=True, index_label="rsID")

