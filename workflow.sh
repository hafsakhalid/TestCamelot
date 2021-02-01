#!/usr/bin/env bash

CONFIG_FILE=${1}
PDF_FILE=${2}
TEMPLATE=${3}

# Get the page count for the passed PDF so we can iterate over pages one by one.
PAGE_COUNT=$(pdfinfo ${PDF_FILE} | grep Pages: | grep -Eo '[0-9]+$')

# Tell bash we want to break lines on linebreaks instead of all whitespace.
IFS=$'\n'

# Grab all of the table search strings from the config file.
for TABLE_NAME in $(cat ${CONFIG_FILE} | egrep title_name | egrep -o '"(.*)"' | sed -n 's/^"\(.*\).*"$/\1/p'); do

    # For every page in the PDF, find if it matches a table search string.
    for i in $(seq ${PAGE_COUNT}); do
        PDF_LINES=$(pdf2txt.py -p ${i} "${PDF_FILE}")

        # Accumulate the matched pages and then pass them to python for extraction.
        RESULT=$(echo ${PDF_LINES} | egrep "${TABLE_NAME}")
        if [[ ${RESULT} ]]; then
            PAGE_LIST="${PAGE_LIST}${i},"
        else
            if [[ ${PAGE_LIST} ]]; then
                # Pass in a list of pages that match the table search string.
                python sureconnect.py ${CONFIG_FILE} ${PDF_FILE} ${PAGE_LIST} ${TEMPLATE} 
                PAGE_LIST=""
            fi
        fi
    done
done

