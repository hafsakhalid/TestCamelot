import camelot 
import pandas as pd 
import csv


tables = camelot.read_pdf('2020.pdf', pages='2', flavor='stream')
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
df = df.drop(df.index[[0,2]])

#loading the correctly recognised table
table = camelot.read_pdf('2020.pdf', pages='1', flavor='stream')
df1 = table[0].df
df1 = df1.drop([0, 1], axis=0)
print(df1)

columns = ['0', '1', '2', '3', '4', '5' , '6', '7', '8'] 
df.columns = columns
df1.columns = columns
#print(df)
#print(df1)

result = pd.concat([df1, df])
print(result)

#out.to_csv('output.csv', index=False)

