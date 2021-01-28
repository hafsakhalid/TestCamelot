import sys
from sys import argv
import rank_din_fix
from pandera.typing import Series
import pandera as pa
import camelot
import logging
import pandas as pd
from openpyxl import load_workbook
#import yaml
import config

#loading config file w yaml
#config  = sys.argv[1]
#config = yaml.safe_load(open("config.yml"))

logging.basicConfig(format='%(message)s', level=logging.INFO)

#script  - just sureconnect (sys.argv[0])
#pdf = 2020.pdf
#template = Renewal Template Proof Zero.xlsm
#pagelist = (will get as input from workflow)
#pdf = '2020.pdf'


#config = sys.argv[1]
#pass the name of the yaml file
pdf = sys.argv[1]
pagelist = sys.argv[2]

print(config.string_match['title_name'])

#this method can be in a different file (ask Alex)
#page is pagelist, not starting page of config file

def extracttable(): 
    tables = camelot.read_pdf(pdf, pages=pagelist, flavor=config.extracts['flavour'])
    df = tables[0].df
    return df

df = extracttable()
print(df)



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
        pa.Check(lambda s: s.str.split("\n", expand=True).shape[0] == 1)])
    
    })
#conditions keeps track of which fix_up has been applied

fix_up = dict()
fix_up['SchemaErrors'] = rank_din_fix.rank_din_fix

#conditions all true for every fix_up
conditions = {e : True for e in fix_up}
while(all(conditions)): 
    try:
        schema.validate(df, lazy=True)
    except Exception as exception: 
        error = pa.errors.SchemaErrors # the schema error names 
        error_name = type(exception).__name__ #errorheadname
    if(not conditions['SchemaErrors']): 
        logging.info("Already tried fix up!")
        break
    else: 
        logging.info("Trying fix up")
        #once you try a fix up, you replace the True with calling the fix_up on df, which goes in not conditions
        conditions['SchemaErrors'] = fix_up['SchemaErrors'](df)
        break #only here because no other fix ups in the list yet 

#updating the df
df = conditions['SchemaErrors']
#this is going to return the dataFrame after tryng all the fix_ups (right now only one fix up so)


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

print(df2)

#Writing to a template
#template should the argument but it does not accept a variable, so ask Alex
template = load_workbook('Renewal Template Proof Zero.xlsm', read_only=False, keep_vba=True)
writer = pd.ExcelWriter('Renewal Template Proof Zero.xlsm', engine='openpyxl')
writer.book = template
writer.sheets = {ws.title: ws for ws in template.worksheets}
#for sheet in writer.sheets: 
    #print(sheet)

df2.to_excel(writer, sheet_name="Accounts", startrow = 1, index=False)
writer.save()



#brute force the files into excel
# table = camelot.read_pdf('2020-ABC Client-Drug Report-Jul-Jun Proof Zero.pdf', pages='1', flavor='stream')
# df3 = table[0].df
# template = load_workbook('Renewal Template Proof Zero.xlsm', read_only=False, keep_vba=True)
# writer = pd.ExcelWriter('Renewal Template Proof Zero.xlsm', engine='openpyxl')
# writer.book = template
# writer.sheets = {ws.title: ws for ws in template.worksheets}
# df3.to_excel(writer, sheet_name="2020-ABC", startrow = 1, index=False)
# writer.save()

# table = camelot.read_pdf('Renewal Example Proof Zero Edited 12_14.pdf', pages='16', flavor='stream')
# df4 = table[0].df
# template = load_workbook('Renewal Template Proof Zero.xlsm', read_only=False, keep_vba=True)
# writer = pd.ExcelWriter('Renewal Template Proof Zero.xlsm', engine='openpyxl')
# writer.book = template
# writer.sheets = {ws.title: ws for ws in template.worksheets}
# df4.to_excel(writer, sheet_name="By Claims", startrow = 1, index=False)

# writer.save()


#try it with 16 and 15 (comes out clean)









   












