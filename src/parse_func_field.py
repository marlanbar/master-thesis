import pandas as pd
import sys

def load_data(ifile):
    data = pd.read_table(ifile,header = None)
    data.columns = ['chrom','chromStart','chromEnd','name','strand','observed','func']
    return data

###### #feature ingeniering  #####
################################## 
## this line is agreggating features in 5prima and 3prima terminals. No estoy seguro si es la mejor decision. Hay un valance que cumplir entre meaning biolpgico y lo sparse que queda la matriz de dummies. Por ejemplo, en el caso de splicing son tan pocos datos y es tan relevante que sea splicing que el hecho de que este en 3prima o en 5prima me chupa un huevo. Ahora no me queda claro que esto valga para todos los kewords. Por ahora avanzamos asi. Dejo la linea que no difenncia entre 3prima y 5prima comentada abajo. 

def get_kewords(df,field='func'): 
    #words = pd.Series(','.join(df.func.values).split(',')).replace({'\\N':'unknown'})  # this approach produce  #15 dummy features
    words = pd.Series(','.join(df.func.values).split(',')).replace({'\\N':'unknown'}).str.replace('-3','').str.replace('-5','')  #this approach produce #12 features
    return words.unique()    

def get_dummies(df,words,field='func'):
    for w in words:
        df[w]=df[field].str.contains(w) + 0
    return df[words]

def saving(df,ofile):
    df.to_csv(ofile,sep = '\t')

    
def main():
    ifile = sys.argv[1]
    data =load_data(ifile)
    words = get_kewords(df = data)
    data_out = get_dummies(df = data,words = words)
    saving(df=data,ofile = ifile.split('.')[0]+'_funcDummie.tsv')

if __name__ == '__main__':
    main()

