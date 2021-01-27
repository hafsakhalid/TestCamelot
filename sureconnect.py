import sys
from sys import argv
import rank_din_fix
from pandera.typing import Series
import pandera as pa
import camelot
import logging
import pandas as pd
from openpyxl import load_workbook



logging.basicConfig(format='%(message)s', level=logging.INFO)
#script  - just sureconnect (sys.argv[0])
#configfile 
#pdf = 2020.pdf
#template = Renewal Template Proof Zero.xlsm
#pagelist = (will get as input from workflow)
#pdf = '2020.pdf'

pdf = sys.argv[1]
pagelist = sys.argv[2]
template = sys.argv[3]

tables = camelot.read_pdf(pdf, pages=pagelist, flavor='stream')
df = tables[0].df

#get standard columns for each df, 
#string for 0 - num of columns
def standardcols(df): 
    cols = list(df.columns)
    for i in cols: 
        cols[i] = str(i)
        df.columns = cols
    return df


df = standardcols(df)
#then you define your schema: 
schema = pa.DataFrameSchema({
    '0': pa.Column(str, checks=[
        # define custom checks as functions that take a series as input and
        # outputs a boolean or boolean Series
        pa.Check(lambda s: s.str.split("\n", expand=True).shape[1] < 2) ])
    
    })

#conditions keeps track of which fix_up has been applied
fix_up = dict()
fix_up['SchemaErrors'] = rank_din_fix.rank_din_fix(df)

conditions = {e : True for e in fix_up}
while(all(conditions)): 
    try:
        schema.validate(df, lazy=True)
    except Exception as exception: 
        error_name = type(exception).__name__
    if(not conditions[error_name]): 
        logging.info("Already tried fix up!")
        break
    else: 
        logging.info("Trying fix up")
        conditions['SchemaErrors'] = fix_up['SchemaErrors']
        break

#updating the df
df = conditions['SchemaErrors']
#this is going to return the dataFrame after tryng all the fix_ups 


#ideally all this will already be in a DataFrame because we called sureconnect on the first page before
table = camelot.read_pdf('2020.pdf', pages='1', flavor='stream')
df1 = table[0].df

df1 = df1.drop([0, 1], axis=0)


#make the columns the same as the scehma
df.columns = df1.columns
df1 = df1.append(df, ignore_index=True)


def fxn(col):
    return ' '.join(col.to_string(index=False).split())
cols = df1[:3].apply(fxn, axis=0)    

df2 = df1[3:].reset_index(drop=True)
df2.columns = list(cols) # don't know if need "list"    

#Writing to a template
#template should the argument but it does not accept spaces, so ask Alex
template = load_workbook('Renewal Template Proof Zero.xlsm')
writer = pd.ExcelWriter('Renewal Template Proof Zero.xlsm' , engine='openpyxl')
writer.book = template
writer.sheets = {ws.title: ws for ws in template.worksheets}
#for sheet in writer.sheets: 
    #print(sheet)

#df2.to_excel(writer, startrow = 1, index=False)
writer.save()










   












