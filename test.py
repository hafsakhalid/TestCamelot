import camelot 
import pandas as pd 
import csv


tables = camelot.read_pdf('2020.pdf', pages='2', flavor='stream')
print(tables[0], 'page2')
print(tables, 'page2')
df = tables[0].df

df[['0', '1', '2']] = df[0].str.split('\n',expand=True)
df = df.drop(columns=[0])
#can remove the headers in the csv
df = df.dropna()
cols = df.columns.tolist() 
#print(cols)

#preappending the sepearted values
for j in range(3):
    i = 1
    cols = [cols[-i]]+cols[:-i]
    #print(cols)
    df = df.reindex(columns=cols)

#dropping values
df = df.drop(df.index[[0]])

#loading the correctly recognised table
table = camelot.read_pdf('2020.pdf', pages='1', flavor='stream')
print(table[0], 'page1')
print(table, 'page1')
df1 = table[0].df
df1 = df1.drop([0, 1], axis=0)

df.columns = df1.columns

df1 = df1.append(df, ignore_index=True)

def fxn(col):
    return ' '.join(col.to_string(index=False).split())

cols = df1[:3].apply(fxn, axis=0)    

df2 = df1[3:].reset_index(drop=True)
df2.columns = list(cols) # don't know if need "list"    
#print((df2))

#df2.to_csv('output.csv', index=False)