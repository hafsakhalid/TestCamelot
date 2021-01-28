from pandera.typing import Series
import pandera as pa
import camelot
import rank_din_fix
import pandas as pd

tables = camelot.read_pdf('Renewal Example Proof Zero Edited 12_14.pdf', pages='16', flavor='stream')
df = tables[0].df
cols = list(df.columns)
for i in cols: 
    cols[i] = str(i)
#print(cols)
df.columns = cols

schema = pa.DataFrameSchema({
    '0': pa.Column(str, checks=[
        # define custom checks as functions that take a series as input and
        # outputs a boolean or boolean Series
        pa.Check(lambda s: s.str.split("\n", expand=True).shape[1] < 2) ])
    
    })

#schema.validate(df) #this one fails
try:
    schema.validate(df, lazy=True)

except pa.errors.SchemaErrors as err:
    print("Schema errors and failure cases:")
    print(err.failure_cases.head())
    print("\nDataFrame object that failed validation:")
    print(err.data.head())

finally:
    df = rank_din_fix.rank_din_fix(df)

schema.validate(df) #this one should pass

table = camelot.read_pdf('2020.pdf', pages='1', flavor='stream')
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

#df2.to_excel('Renewal Template Proof Zero.xlsm', sheet_name="amount")

f = pd.ExcelWriter('Renewal Template Proof Zero.xlsm', mode='a')
df2.to_excel(f, sheet_name='amount')














