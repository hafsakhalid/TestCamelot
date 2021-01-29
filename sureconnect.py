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
import logging

from pandera.typing import Series
import pandera as pa
import camelot
import pandas as pd
from openpyxl import load_workbook
import yaml

import functionmap as fm

logging.basicConfig(format="%(message)s", level=logging.INFO)

# First parameter is the config file for this MGA.
config_filename = sys.argv[1]

# # Second parameter is the current PDF we're parsing.
pdf_file = sys.argv[2]

# # Third parameter is the page of the PDF to parse.
page_number = sys.argv[3]

# # Fourth parameter is the template to populate.
template_file = sys.argv[4]

#loading config file w yaml
config  = sys.argv[1]
config = yaml.safe_load(open(config_filename))


# Get all of the tables in the PDF on the indicated page.
tables = camelot.read_pdf( pdf_file, pages=page_number, flavor=config['extracts']['flavour'])

# Standardize columns for stitching, by changing the column headers to string,
# so even before getting the first table, each column name is a string
for table in tables: 
    table.df.columns = table.df.columns.astype(str)


def create_schema(config=config):
    schema = pa.DataFrameSchema()
    columns = [str(i) for i in range(0, config['schema_dict']['num_cols'])]
    for cols in columns:
        schema.checks = [pa.Check(check_fn=fm.fxn_map[value], error=key) for key, value in config['schema_dict']['checks'].items()]
        schema.columns[cols] = pa.Column(pa.String)
    return schema


# Then you define your schema for each pdf, this should take in a tableList 
# def define_schema(tableList=tables):
#     """
#     Define a schema for each table in the PDF and see if it passes or fails 
   
#     """
#     schema = pa.DataFrameSchema({
#         '0':pa.Column(
#             pa.String, 
#             checks = [
#                 pa.Check(lambda s : s.str.contains('\n') == True, error="StringError")
#             ]),
#         })

    # Define the condtions dicitonary as True
    
#TO:DO The column number for both the pages are different, so error
def apply_schema(schema=create_schema(), tableList=tables, config=config):
    return_tables = []
    for table in tables:
        # We have a list of fixable errors and we try each of them once
        # if the current table needs them.
        conditions = {error_fixable : True for error_fixable in config['fix_ups']}
        while(any(conditions.values())):
            try:
                schema.validate(table.df, lazy=True)
                return return_tables
            except pa.errors.SchemaErrors as errors:
                error_name = str(errors.failure_cases['check'][0]) 
                if(not conditions[error_name]):
                    raise Exception ('Schema fixups failed: already tried fixup.')
                    break
                elif(conditions[error_name]):
                    return_tables.append(fm.fxn_map[config['fix_ups'][error_name]](table.df))
                    conditions[error_name] = False
                else:
                    raise Exception ('Schema fixups failed: unexpected error.')

        return return_tables


return_tables = apply_schema()
final_df = pd.DataFrame()
final_df = pd.concat([df for df in return_tables], ignore_index=True)

# Writing to a template
# template should the argument but it does not accept a variable, so ask Alex
def output_template(df=final_df, template=template_file, engine="openpyxl", lib=pd.ExcelWriter): 
    #should import loadworkbook
    output = load_workbook (
        template, read_only=False, keep_vba=True
    )
    writer = pd.ExcelWriter("outfile.xlsm", engine=engine)
    writer.book = output
    final_df.to_excel(writer, sheet_name="Accounts", startrow=1, index=False)
    writer.save()

output_template()

if __name__ == "__main__":
    import sys
    import doctest

    # Return the number of doctests that fail. This gives calling scripts
    # a non-zero exit code if there are failing tests.
    sys.exit(doctest.testmod(verbose=True)[0])
