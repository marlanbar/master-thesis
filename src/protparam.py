import gzip
import pandas as pd
import numpy as np
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio import SwissProt
from Bio import SeqIO

from functools import partial


DATA_EXTERNAL = "../data/external/"
DATA_PROCESSED = "../data/processed/"
DATA_INTERIM = "../data/interim/"

GT = pd.read_csv(DATA_PROCESSED + "processed/humsavar_gt.csv.gz", index_col="MUTANT")
uniprots = pd.DataFrame.from_items(zip(GT.index, GT.index.str.split("-"))).T
uniprots.columns = ["uniprot", "position", "amino", "amino_var"]
uniprots.position = uniprots.position.astype(int)


# Reads FASTA file with human proteome, and sequences a to file for easier Pandas reading.
sequences = open(DATA_INTERIM + "human_prot_sequences.txt", "w")
for e, record in enumerate(SeqIO.parse(DATA_FOLDER + "uniprot-proteome%3AUP000005640.fasta", "fasta")):
    uni_id = record.id.split("|")[1]
    sequences.write("%s,%s\n" % (uni_id, record.seq))
    
    
sequences = pd.read_csv(DATA_INTERIM + "interim/human_prot_sequences.txt", header=None, names=["uniprot", "sequence"])

uniprots = uniprots.reset_index().merge(sequences, on="uniprot").set_index("index")

# Extracts subsequence and applies variation. 
# If var == False, it doesn't replace the aminoacid. 
# With width == -1, then the whole sequence is returned.
def get_subsequence(row, width=1, var=True):
    seq = row['sequence']
    pos = row['position']-1
    if (width != -1 and var):
        return seq[pos-width:pos] + row['amino_var'] + seq[pos+1:pos+width+1]
    if (width != -1 and  not var):
        return seq[pos-width:pos] + seq[pos-1:pos+width+1]
    if (width == -1 and var):
        return seq[:pos] + row['amino_var'] + seq[pos+1:]
    
uniprots['slice'] = uniprots.apply(partial(get_subsequence, width=7, var=False), axis=1)
uniprots['var_slice'] = uniprots.apply(partial(get_subsequence, width=7), axis=1)

uniprots[["var_slice", "slice"]].to_csv(DATA_INTERIM + "humsavar_gt_protein_slices.csv.gz", 
                                        index=True, index_label="MUTANT", compression="gzip")

uniprots = pd.read_csv(DATA_INTERIM + "humsavar_gt_protein_slices.csv.gz")

def get_protparam(row, func_name):
    protein_analysis = ProteinAnalysis(row)
    try:
        param = getattr(protein_analysis, func_name)()
        return param
    except:
        return np.nan
        

params = ["aromaticity", "isoelectric_point", "gravy", "instability_index"]

for param in params:
    uniprots[('var_' + param)] = uniprots.var_slice.apply(partial(get_protparam, func_name=param))
    uniprots[param] = uniprots.slice.apply(partial(get_protparam, func_name=param))
    uniprots[param + "_diff"] =  abs(uniprots[param] - uniprots[('var_' + param)])
    uniprots[param + "_log_ratio"] = np.log((uniprots[param] + 1) / (uniprots[('var_' + param)] + 1))
    
uniprots.columns = uniprots.columns.map(lambda x: x.upper())
uniprots.drop("SLICE", 1).drop("VAR_SLICE",1).to_csv(DATA_INTERIM + "protparam_features.csv.gz", index=False, compression="gzip")