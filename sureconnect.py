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
#import logging

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

# Get all of the tables in the PDF on the indicated page.
tables = camelot.read_pdf( pdf_file, pages=page_number, flavor=config.extracts['flavour'])

# Standardize columns for stitching, by changing the column headers to string,
# so even before getting the first table, each column name is a string
for table in tables: 
    table.df.columns = table.df.columns.astype(str)

# Then you define your schema for each pdf, this should take in a tableList 
def define_schema(tableList=tables):
    """
    Define a schema for each table in the PDF and see if it passes or fails 
   
    """
    schema = pa.DataFrameSchema({
        '0':pa.Column(
            pa.String, 
            checks = [
                pa.Check(lambda s : s.str.contains('\n') == True, error="StringFailure")
            ]),
        })

    # Define the condtions dicitonary as True
    conditions = {col.name : True for col in schema.columns}
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
                conditions[check_number] = False
                break
    
    return tableList

# This applies the schema to all the tables in the tablelist, an outputs a dataFrame
final_df = pd.DataFrame()
for table in tables: 
    final_df = final_df.append(define_schema(table.df), ignore_index=True)

# Writing to a template
# template should the argument but it does not accept a variable, so ask Alex

def output_template(df=final_df, template=template_file, engine="openpyxl", lib=pd.ExcelWriter): 
    #should import loadworkbook
    output = load_workbook (
        template, read_only=False, keep_vba=True
    )
    writer = pd.ExcelWriter("outfile.xlsm", engine=engine)
    writer.book = output
    #writer.sheets = {ws.title: ws for ws in template.worksheets}
    final_df.to_excel(writer, sheet_name="Accounts", startrow=1, index=False)
    writer.save()

output_template()

if __name__ == "__main__":
    import sys
    import doctest

    # Return the number of doctests that fail. This gives calling scripts
    # a non-zero exit code if there are failing tests.
    sys.exit(doctest.testmod(verbose=True)[0])
