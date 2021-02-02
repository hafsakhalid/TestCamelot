#!/usr/bin/env bash
cp output_template.xlsx output.xlsx
./workflow.sh config.yaml 2020.pdf Renewal\ Template\ Proof\ Zero.xlsm
./workflow.sh config.yaml 2020-ABC\ Client-Drug\ Report-Jul-Jun\ Proof\ Zero.pdf Renewal\ Template\ Proof\ Zero.xlsm
./workflow.sh config.yaml Renewal\ Example\ Proof\ Zero\ Edited\ 12_14.pdf Renewal\ Template\ Proof\ Zero.xlsm
echo "PDF data extraction and template mapping complete."
open output.xlsx
say "Extracted three tables to Excel."
