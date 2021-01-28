#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Proof Zero, Inc. 2021
# pylint: disable=C0301,W0621,C0116,C0103
# pylint: disable=W0703,R1723,E0110,W0404,W0611,C0411,C0412
"""
End-to-end implementation for extracting tabular data from PDFs and appending
it to a given Excel template.
"""
import sys
import pdb
import doctest
from sys import argv
#importlogging

from pandera.typing import Series
import pandera as pa
import camelot
import pandas as pd
from openpyxl import load_workbook
# import yaml

import rank_din_fix

#logging.basicConfig(format="%(message)s", level=logging.INFO)

# First parameter is the config file for this MGA.
config_filename = sys.argv[1]

# # Second parameter is the current PDF we're parsing.
pdf_file = sys.argv[2]

# # Third parameter is the page of the PDF to parse.
page_number = sys.argv[3]

# # Fourth parameter is the template to populate.
template_file = sys.argv[4]

# TODO: loading config file w yaml
import config
# config  = sys.argv[1]
# config = yaml.safe_load(open(config_filename))
# print(config.string_match["title_name"])

tables = camelot.read_pdf( pdf_file, pages=page_number, flavor=config.extracts['flavour'])
#df = tables[0].df

#def mock_read_pdf(pdf_filename, pages, flavor):
#    from types import SimpleNamespace
#    frame = pd.DataFrame({'A': [pdf_filename, pages, flavor]})
#    wrapper = { 'df': frame }
#    tables = list()
#    tables.append(SimpleNamespace(**wrapper))
#    return tables
#
#def extract_tables(pdf_filename=pdf_file, pages=page_number, flavour="stream", read_pdf=camelot.read_pdf):
#    """
#    Extract tables from the given page of a PDF.
#    
#    >>> extract_tables(123, 456, 789, mock_read_pdf)
#         A
#    0  123
#    1  456
#    2  789
#
#    >>> extract_tables(pdf_file, page_number, config.extracts['flavour'], camelot.read_pdf) # doctest: +NORMALIZE_WHITESPACE
#         0                                       1                                      2   3            4            5
#    0                                                                                      To  30-Jun-2019  30-Jun-2020
#    1                   Average Number of Insureds                                                      86           82
#    2   A)                           Paid Premiums                                                $258,497     $230,125
#    3                            Adjusted Premiums                                                $241,033     $230,125
#    4                (excludes plan change impact)
#    5                             Pooling Premiums                                               $(42,864)    $(40,924)
#    6       Quebec Drug Insurance Pooling Premiums                                                       –            –
#    7   B)            Non Pooled Adjusted Premiums                                                $198,169     $189,201
#    8               Paid Claims (Net of Cost Plus)                                                $135,098     $139,511
#    9                       Normalized Paid Claims                                                $135,098     $150,672
#    10                              Pooling Credit                                                  $(261)       $(220)
#    11        Quebec Drug Insurance Pooling Credit                                                       –            –
#    12                      Change in IBNR Reserve                                                $(2,336)         $356
#    13  C)              Non Pooled Incurred Claims                                                $132,501     $150,808
#    14  D)                              Loss Ratio                                                   66.9%        79.7%
#    15  E)                                   Trend                                                   29.0%        15.7%
#    16  F)                        Retention Factor                                                   22.4%        22.4%
#    17  G)                     Adjusted Loss Ratio                                                  111.2%       118.8%
#    18  H)                               Weighting                                                   25.0%        75.0%
#    19                                                                Weighted Loss Ratio                        116.9%
#    20                                                                        Credibility                        100.0%
#    21                                              Adjusted Loss Ratio after Credibility                        116.9%
#    22                                                                   Final Loss Ratio                        117.0%
#    23                                                                    Rate Adjustment                           17%
#    24                                                              Final Rate Adjustment                           17%
#
#    """
#    return read_pdf(pdf_filename, pages=pages, flavor=flavour)
#
#pdb.set_trace()
#df = extract_tables(pdf_file, page_number, config.extracts['flavour'], camelot.read_pdf)

#df = tables[0].df
#print(df)

# get standard columns for each df,
# string for 0 - num of columns


#def standardcols(dataFrame=df):
    
    # """ Should return df columns as a string 


    # >>> standardcols() # doctest: +NORMALIZE_WHITESPACE
    #          0                                       1                                      2   3            4            5
    # 0                               Period Covered                                                                     
    # 1                                                                                      To  30-Jun-2019  30-Jun-2020
    # 2                   Average Number of Insureds                                                      86           82
    # 3   A)                           Paid Premiums                                                $258,497     $230,125
    # 4                            Adjusted Premiums                                                $241,033     $230,125
    # 5                (excludes plan change impact)                                                                     
    # 6                             Pooling Premiums                                               $(42,864)    $(40,924)
    # 7       Quebec Drug Insurance Pooling Premiums                                                       –            –
    # 8   B)            Non Pooled Adjusted Premiums                                                $198,169     $189,201
    # 9               Paid Claims (Net of Cost Plus)                                                $135,098     $139,511
    # 10                      Normalized Paid Claims                                                $135,098     $150,672
    # 11                              Pooling Credit                                                  $(261)       $(220)
    # 12        Quebec Drug Insurance Pooling Credit                                                       –            –
    # 13                      Change in IBNR Reserve                                                $(2,336)         $356
    # 14  C)              Non Pooled Incurred Claims                                                $132,501     $150,808
    # 15  D)                              Loss Ratio                                                   66.9%        79.7%
    # 16  E)                                   Trend                                                   29.0%        15.7%
    # 17  F)                        Retention Factor                                                   22.4%        22.4%
    # 18  G)                     Adjusted Loss Ratio                                                  111.2%       118.8%
    # 19  H)                               Weighting                                                   25.0%        75.0%
    # 20                                                                Weighted Loss Ratio                        116.9%
    # 21                                                                        Credibility                        100.0%
    # 22                                              Adjusted Loss Ratio after Credibility                        116.9%
    # 23                                                                   Final Loss Ratio                        117.0%
    # 24                                                                    Rate Adjustment                           17%
    # 25                                                              Final Rate Adjustment                           17%
     
    # """



#Standardize columns for stitching, by changing the column headers to string, so even before getting the first table, each column name is a string
for table in tables: 
    table.df.columns = table.df.columns.astype(str)


#then you define your schema for each pdf, this should take in a tableList 
def define_schema(tableList=tables):
    # """ Define a schema for each table in the PDF and see if it passes or fails 
    
    # >>> define_schema(tables[0].df)
    # Trying fix_up
    #      0                                       1                                      2   3            4            5
    # 0                               Period Covered                                                                     
    # 1                                                                                      To  30-Jun-2019  30-Jun-2020
    # 2                   Average Number of Insureds                                                      86           82
    # 3   A)                           Paid Premiums                                                $258,497     $230,125
    # 4                            Adjusted Premiums                                                $241,033     $230,125
    # 5                (excludes plan change impact)                                                                     
    # 6                             Pooling Premiums                                               $(42,864)    $(40,924)
    # 7       Quebec Drug Insurance Pooling Premiums                                                       –            –
    # 8   B)            Non Pooled Adjusted Premiums                                                $198,169     $189,201
    # 9               Paid Claims (Net of Cost Plus)                                                $135,098     $139,511
    # 10                      Normalized Paid Claims                                                $135,098     $150,672
    # 11                              Pooling Credit                                                  $(261)       $(220)
    # 12        Quebec Drug Insurance Pooling Credit                                                       –            –
    # 13                      Change in IBNR Reserve                                                $(2,336)         $356
    # 14  C)              Non Pooled Incurred Claims                                                $132,501     $150,808
    # 15  D)                              Loss Ratio                                                   66.9%        79.7%
    # 16  E)                                   Trend                                                   29.0%        15.7%
    # 17  F)                        Retention Factor                                                   22.4%        22.4%
    # 18  G)                     Adjusted Loss Ratio                                                  111.2%       118.8%
    # 19  H)                               Weighting                                                   25.0%        75.0%
    # 20                                                                Weighted Loss Ratio                        116.9%
    # 21                                                                        Credibility                        100.0%
    # 22                                              Adjusted Loss Ratio after Credibility                        116.9%
    # 23                                                                   Final Loss Ratio                        117.0%
    # 24                                                                    Rate Adjustment                           17%
    # 25                                                              Final Rate Adjustment                           17%
    
    
    # """
    schema = pa.DataFrameSchema({
        '0':pa.Column(
            pa.String, 
            checks = [
                pa.Check(lambda s : s.str.contains('\n') == True)
            ]),    
        })
    #define the condtions dicitonary as True
    fix_up = dict()
    fix_up['0'] = 10 #arbritary value for now
    conditions = {e : True for e in fix_up}
    
    while(all(conditions)):
        try:
            schema.validate(tableList, lazy=True)
        except pa.errors.SchemaErrors as errors:
            check_number = str(errors.failure_cases['column'][0]) 
            #this is the column number that fails the check, need this as a key, so change to str
            if(not conditions[check_number]): 
                print("Already tried fix_up")
                break
            else: 
                print("Trying fix_up")
                conditions[check_number] = fix_up[check_number]#(tableList)
                break #ask Alex why this does not quit the while loop
    
    return tableList

#this applies the schema to all the tables in the tablelist, an outputs a dataFrame
final_df = pd.DataFrame()
for table in tables: 
    final_df = final_df.append(define_schema(table.df), ignore_index=True)



# Writing to a template
# template should the argument but it does not accept a variable, so ask Alex

def output_template(df=final_df, template=template_file, engine="openpyxl", lib=pd.ExcelWriter): 
    #should import loadworkbook
    output = load_workbook (
        "Renewal Template Proof Zero.xlsm", read_only=False, keep_vba=True
    )
    writer = pd.ExcelWriter("Renewal Template Proof Zero.xlsm", engine=engine)
    writer.book = output
    writer.sheets = {ws.title: ws for ws in template.worksheets}
    final_df.to_excel(writer, sheet_name="Accounts", startrow=1, index=False)
    writer.save()


if __name__ == "__main__":
    import sys
    import doctest

    # Return the number of doctests that fail. This gives calling scripts
    # a non-zero exit code if there are failing tests.
    sys.exit(doctest.testmod(verbose=True)[0])
