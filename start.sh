#!/usr/bin/env bash
echo "Beginning data extraction and template mapping."
# say "Beginning data extraction and template mapping." &
cp output_template.xlsx output.xlsx
./workflow.sh config.yaml 2020.pdf Renewal\ Template\ Proof\ Zero.xlsm
./workflow.sh config.yaml 2020-ABC\ Client-Drug\ Report-Jul-Jun\ Proof\ Zero.pdf Renewal\ Template\ Proof\ Zero.xlsm
./workflow.sh config.yaml Renewal\ Example\ Proof\ Zero\ Edited\ 12_14.pdf Renewal\ Template\ Proof\ Zero.xlsm
echo "PDF data extraction and template mapping complete."
# say "PDF data extraction and template mapping complete. Extracted three tables to Excel." &
open output.xlsx
