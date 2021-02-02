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

import pandera as pa
from pandera.errors import SchemaErrors

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

# # Third parament is the name of the table from the config so we can filter the config file.
config_table_section = sys.argv[3]

# # Next parameter is the page of the PDF to parse.
# # Shave the trailing comma off the passed list.
page_numbers = (sys.argv[4])[:-1]

# # Last parameter is the template to populate.
template_file = sys.argv[5]

#loading config file w yaml
configs = yaml.safe_load(open(config_filename))

def create_schema(config):
    schema = pa.DataFrameSchema()
    columns = [str(i) for i in range(0, config['schema_dict']['num_cols'])]
    for col in columns:
        schema.checks = [pa.Check(check_fn=fm.fxn_map[value], error=key) for key, value in config['schema_dict']['checks'].items()]
        schema.columns[col] = pa.Column(pa.String, name=col)
    return schema

def apply_schema(schema, tableList, config):
    return_frames = []
    for table in tableList:
        df = table.df
        try:
            schema.validate(df, lazy=True)
        except SchemaErrors as errors:
            checklist = set([check for check in errors.failure_cases['check']])
            for item in checklist:
                df = fm.fxn_map[config['fix_ups'][item]](df)
        return_frames.append(df)
    return return_frames

def filter_rows(row, cutoff):
    # Get the percent of the row that is populated.
    sparseness = row.str.count('^.+$').sum() / len(row)
    if sparseness < cutoff:
        pass
    else:
        return(row)

def output_template(df, template, config, columns, engine="openpyxl"):
    df.to_excel(config['template_map']['dst_book'], sheet_name=config['template_map']['dst_sheet'], index=False, header=False)#columns)
    output = load_workbook (
        'output.xlsx', read_only=False, keep_vba=False
    )
    writer = pd.ExcelWriter('output.xlsx', engine=engine)
    writer.book = output
    df.to_excel(writer, sheet_name=config['template_map']['dst_sheet'], startrow=0, index=False, header=False)#columns)
    writer.save()


for i, e in enumerate(configs['tables']):
    for k, config in configs['tables'][i].items():
        if (config['string_match']['title_name'] != config_table_section):
            continue
        # Get all of the tables in the PDF on the indicated pages.
        tables = camelot.read_pdf(pdf_file, pages=page_numbers, flavor=config['extracts']['flavour'])
        sparse_filter = config['extracts']['sparse_filter']

        # Standardize columns for stitching, by changing the column headers to string,
        # so even before getting the first table, each column name is a string
        columns = None
        for table in tables:
            # Apply our config choice for filtering out sparse rows.
            # This helps identify multi-row column headers and summary sections.
            table.df = table.df.apply(filter_rows, axis=1, args=(sparse_filter,), result_type='broadcast').dropna()
            columns = table.df[:1]
            #print(columns)
            table.df = table.df[1:].reset_index(drop=True)
            table.df.columns = table.df.columns.astype(str)
    
        schema = create_schema(config)
        return_tables = apply_schema(schema=schema, tableList=tables, config=config)
        final_df = pd.concat(return_tables, ignore_index=True)
        output_template(final_df, template_file, config, columns)


if __name__ == "__main__":
    import sys
    import doctest

    # Return the number of doctests that fail. This gives calling scripts
    # a non-zero exit code if there are failing tests.
    #sys.exit(doctest.testmod(verbose=True)[0])
