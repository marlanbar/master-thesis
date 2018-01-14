import pandas as pd

DATA_EXTERNAL = "../data/external/"
DATA_PROCESSED = "../data/processed/"
DATA_INTERIM = "../data/interim/"


#Levanto tabla limpia de humsavar
print("Loading humsavar table...")
hum = pd.read_csv(DATA_INTERIM + "humsavar_clean_201711.csv.gz", sep=",")
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
df = pd.DataFrame(data=(hum["AA_Change"].str[2:].str.split(r"([0-9]+)")).tolist(), columns=["C1", "C2", "C3"])
df["C1"] = df.C1.map(AMINO_CODE)
df["C3"] = df.C3.map(AMINO_CODE)
mutant = pd.Series(data=(hum["Swiss_Prot_AC"] + "-" + df.C2 
                         + "-" + df.C1 + "-" + df.C3).tolist(), name="MUTANT")

hum_final = pd.concat([hum, mutant], 1)[["Type_of_variant", "MUTANT", "dbSNP"]]
hum_final.rename(columns={"Type_of_variant": "TYPE"}, inplace=True)

# Mergeo features
print("Merging features...")
print("VARQ")
#varQ
varq = pd.read_csv(DATA_PROCESSED + "properties-varq.tab.gz", sep="\t").drop("TYPE", axis=1)
humsavar_gt = varq.merge(hum_final, left_on="MUTANT", right_on="MUTANT", how="inner")

print("PROTPARAM")
#ProtParam
protparam = pd.read_csv(DATA_INTERIM + "protparam_features.tab.gz", sep="\t")
humsavar_gt = humsavar_gt.merge(protparam, on="MUTANT", how="left")

print("46-WAY-CONSERVATION")
#Conservation (46-way primates)
cons46way = pd.read_csv("../data/interim/cons46way.csv")
humsavar_gt = humsavar_gt.merge(cons46way, on="dbSNP", how="left")

humsavar_gt.to_csv(DATA_PROCESSED + "humsavar_gt.csv.gz", index=False, compression="gzip")





