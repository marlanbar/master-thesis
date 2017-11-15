# coding: utf-7

import pandas as pd
import numpy as np
import argparse

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
    df = pd.DataFrame(data=res, columns=cols).replace("-", np.nan)
    df.to_csv(args.output, sep=args.separator, index=False, header=True, compression="gzip")

