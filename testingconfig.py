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


















# ideally all this will already be in a DataFrame because we called sureconnect on the first page before
table = camelot.read_pdf("2020.pdf", pages="1", flavor="stream")
df1 = table[0].df

df1 = df1.drop([0, 1], axis=0)

# make the columns the same as the scehma
df.columns = df1.columns
df1 = df1.append(df, ignore_index=True)


def fxn(col):
    return " ".join(col.to_string(index=False).split())


cols = df1[:3].apply(fxn, axis=0)

df2 = df1[3:].reset_index(drop=True)
df2.columns = list(cols)  # don't know if need "list"

print(df2)

# Writing to a template
# template should the argument but it does not accept a variable, so ask Alex
template = load_workbook(
    "Renewal Template Proof Zero.xlsm", read_only=False, keep_vba=True
)
writer = pd.ExcelWriter("Renewal Template Proof Zero.xlsm", engine="openpyxl")
writer.book = template
writer.sheets = {ws.title: ws for ws in template.worksheets}
# for sheet in writer.sheets:
# print(sheet)

df2.to_excel(writer, sheet_name="Accounts", startrow=1, index=False)
writer.save()


# brute force the files into excel
table = camelot.read_pdf(
    "2020-ABC Client-Drug Report-Jul-Jun Proof Zero.pdf",
    pages="1",
    flavor="stream",
)
df3 = table[0].df
template = load_workbook(
    "Renewal Template Proof Zero.xlsm", read_only=False, keep_vba=True
)
writer = pd.ExcelWriter("Renewal Template Proof Zero.xlsm", engine="openpyxl")
writer.book = template
writer.sheets = {ws.title: ws for ws in template.worksheets}
df3.to_excel(writer, sheet_name="2020-ABC", startrow=1, index=False)
writer.save()

table = camelot.read_pdf(
    "Renewal Example Proof Zero Edited 12_14.pdf", pages="16", flavor="stream"
)
df4 = table[0].df
template = load_workbook(
    "Renewal Template Proof Zero.xlsm", read_only=False, keep_vba=True
)
writer = pd.ExcelWriter("Renewal Template Proof Zero.xlsm", engine="openpyxl")
writer.book = template
writer.sheets = {ws.title: ws for ws in template.worksheets}
df4.to_excel(writer, sheet_name="By Claims", startrow=1, index=False)

writer.save()


# try it with 16 and 15 (comes out clean)

if __name__ == "__main__":
    import sys
    import doctest

    # Return the number of doctests that fail. This gives calling scripts
    # a non-zero exit code if there are failing tests.
    sys.exit(doctest.testmod(verbose=True)[0])

sys.exit(0)