# coding: utf-7
import pandas as pd
import numpy as np
import re
import argparse
import config

def parse_args():
    parser = argparse.ArgumentParser(description="Return a pandas compatible version of humsavar.txt")
    parser.add_argument("--file", "-f", required=True, help="Clean humsavar file without prologue, header and coda")                               
    parser.add_argument("--separator",  "-s", required=False, default=",", help="Table separator")
    parser.add_argument("--output", "-o", required=True, help="Output file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    cols = ["Main gene name", "Swiss Prot AC", "FTId", "AA Change", 
            "Type of variant", "dbSNP", "Disease Name"]
    
    # Receives humsavar file without intro, header and  tail info
    f = open(args.file)
    res = []
    for i, l in enumerate(f):
        l = ' '.join(l.split())
        res.append(l.split(" ", 6))
    hum = pd.DataFrame(data=res, columns=cols).replace("-", np.nan)
    hum.columns = hum.columns.str.replace(" ", "_")

    #Correspondencia hecha por Santi
    AMINO_CODE = {"Ala": "A",\
                  "Arg": "R",\
                  "Asn": "N",\
                  "Asp": "D",\
                  "Cys": "C",\
                  "Gln": "Q",\
                  "Glu": "E",\
                  "Gly": "G",\
                  "His": "H",\
                  "Ile": "I",\
                  "Leu": "L",\
                  "Lys": "K",\
                  "Met": "M",\
                  "Phe": "F",\
                  "Pro": "P",\
                  "Ser": "S",\
                  "Thr": "T",\
                  "Trp": "W",\
                  "Tyr": "Y",\
                  "Val": "V",\
                  "Sec": "U"
    }

    #Transformo la columna de Uniprot a MUTANT (Uniprot-Posicion-Amino original-Nuevo Amino)
    print("Processing table...")
  
    print(hum.head(2).AA_Change)
    amino = hum.head(2).AA_Change.str[2:].str.extract(r"p.(?P<C1>[A-Z]{1}[a-z]{2})(?P<C2>\d+)(?P<C3>[A-Z]{1}[a-z]{2})", expand=True)
    print(amino)
    # df["C1"] = df.C1.map(AMINO_CODE)
    # df["C3"] = df.C3.map(AMINO_CODE)
    #mutant = pd.Series(data=(hum["Swiss_Prot_AC"] + "-" + df.C3 + "-" + df.C1 + "-" + df.C3).tolist(), name="MUTANT")

    #humsavar_gt = pd.concat([hum, mutant], 1)[["Type_of_variant", "MUTANT", "dbSNP"]]
    #humsavar_gt.rename(columns={"Type_of_variant": "TYPE"}, inplace=True)

    #humsavar_gt.to_csv(args.output, sep=args.separator, index=False, header=True, compression="gzip")

