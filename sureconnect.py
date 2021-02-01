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
# # Shave the trailing comma off the passed list.
page_numbers = (sys.argv[3])[:-1]

# # Fourth parameter is the template to populate.
template_file = sys.argv[4]

#loading config file w yaml
configs = yaml.safe_load(open(config_filename))

def create_schema(config):
    schema = pa.DataFrameSchema()
    columns = [str(i) for i in range(0, config['schema_dict']['num_cols'])]
    for cols in columns:
        schema.checks = [pa.Check(check_fn=fm.fxn_map[value], error=key) for key, value in config['schema_dict']['checks'].items()]
        schema.columns[cols] = pa.Column(pa.String)
    return schema

#TO:DO The column number for both the pages are different, so error
def apply_schema(schema, tableList, config):
    return_tables = []
    for table in tableList:
        # We have a list of fixable errors and we try each of them once
        # if the current table needs them.
        conditions = {error_fixable : True for error_fixable in config['fix_ups']}
        while(any(conditions.values())):
            try:
                schema.validate(table.df, lazy=True)
                return_tables.append(table.df)
                return return_tables
            except pa.errors.SchemaErrors as errors:
#            except SchemaErrors as err:
#                err.failure_cases  # dataframe of schema errors
#                err.data  # invalid dataframe
                error_name = str(errors.failure_cases['check'][0])
                if(not conditions[error_name]):
                    raise Exception ('Schema fixups failed: already tried fixup.')
                elif(conditions[error_name]):
                    table.df = fm.fxn_map[config['fix_ups'][error_name]](table.df)
                    conditions[error_name] = False
                    try:
                        schema.validate(table.df, lazy=True)
                        conditions[error_name] = True
                    except:
                        continue
                else:
                    raise Exception ('Schema fixups failed: unexpected error.')

    return return_tables


for i, e in enumerate(configs['tables']):
    for k, config in configs['tables'][i].items():
        # Get all of the tables in the PDF on the indicated pages.
        final_df = pd.DataFrame()

        tables = camelot.read_pdf(pdf_file, pages=page_numbers, flavor=config['extracts']['flavour'])

        # Standardize columns for stitching, by changing the column headers to string,
        # so even before getting the first table, each column name is a string
        for table in tables:
            table.df = table.df[4:]
            table.df.columns = table.df.columns.astype(str)
       
        schema = create_schema(config)
        return_tables = apply_schema(schema=schema, tableList=tables, config=config)
        print(return_tables)
        sys.exit(0)

#output the correct table with fix_ups but very overfitted to page2 of the pdf
#final_df = pd.concat([df for df in return_tables])

# Writing to a template
# template should the argument but it does not accept a variable, so ask Alex
def output_template(df=final_df, template=template_file, engine="openpyxl"): 
    #should import loadworkbook
    output = load_workbook (
        template, read_only=False, keep_vba=True
    )
    writer = pd.ExcelWriter("outfile.xlsm", engine=engine)
    writer.book = output
    final_df.to_excel(writer, sheet_name="Accounts", startrow=1, index=False)
    writer.save()

#output_template()


if __name__ == "__main__":
    import sys
    import doctest

    # Return the number of doctests that fail. This gives calling scripts
    # a non-zero exit code if there are failing tests.
    sys.exit(doctest.testmod(verbose=True)[0])
