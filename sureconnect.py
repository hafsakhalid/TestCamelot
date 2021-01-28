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

# Second parameter is the current PDF we're parsing.
pdf_file = sys.argv[2]

# Third parameter is the page of the PDF to parse.
page_number = sys.argv[3]

# Fourth parameter is the template to populate.
template_file = sys.argv[4]

# TODO: loading config file w yaml
import config
# config  = sys.argv[1]
# config = yaml.safe_load(open(config_filename))
# print(config.string_match["title_name"])

pdf = pdf_file
pagelist = page_number

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

tables = camelot.read_pdf(pdf_file, page_number, config.extracts['flavour'])
df = tables[0].df
#print(df)

#if __name__ == "__main__":
#    import sys
#    import doctest
#
#    # Return the number of doctests that fail. This gives calling scripts
#    # a non-zero exit code if there are failing tests.
#    sys.exit(doctest.testmod(verbose=True)[0])
#
#sys.exit(0)
#
# get standard columns for each df,
# string for 0 - num of columns

def standardcols(df):
    # df.columns = df.columns.apply(str)
    cols = list(df.columns)
    for i in cols:
        cols[i] = str(i)
        df.columns = cols
    return df

# Standardize columns for stitching.
for table in tables:
    tables[table].df = standardcols(tables[table].df)

sys.exit(0)

# then you define your schema:
schema = pa.DataFrameSchema(
    {
        "0": pa.Column(
            str,
            checks=[
                # define custom checks as functions that take a series as input and
                pa.Check(lambda s: s.str.split("\n", expand=True).shape[0] == 1)
            ],
        )
    }
)
# conditions keeps track of which fix_up has been applied

fix_up = dict()
fix_up["SchemaErrors"] = rank_din_fix.rank_din_fix

conditions = {e: True for e in fix_up}
while all(conditions):
    try:
        schema.validate(df, lazy=True)
    except Exception as exception:
        error_name = type(exception).__name__  # errorheadname
    if not conditions["SchemaErrors"]:
        logging.info("Already tried fix up!")
        break
    else:
        logging.info("Trying fix up")
        conditions["SchemaErrors"] = fix_up["SchemaErrors"](df)
        break  # only here because no other fix ups in the list yet

# updating the df
df = conditions["SchemaErrors"]
# this is going to return the dataFrame after tryng all the fix_ups


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