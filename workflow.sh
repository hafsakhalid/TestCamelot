#!/usr/bin/env bash
cp output_template.xlsx output.xlsx

CONFIG_FILE=${1}
PDF_FILE=${2}
TEMPLATE=${3}

# Get the page count for the passed PDF so we can iterate over pages one by one.
PAGE_COUNT=$(pdfinfo "${PDF_FILE}" | grep Pages: | grep -Eo '[0-9]+$')

# Tell bash we want to break lines on linebreaks instead of all whitespace.
IFS=$'\n'

# Grab all of the table search strings from the config file.
for TABLE_NAME in $(cat ${CONFIG_FILE} | egrep title_name | egrep -o '"(.*)"' | sed -n 's/^"\(.*\).*"$/\1/p'); do
    START_PAGE=$(cat ${CONFIG_FILE} | grep -A1 ${TABLE_NAME} | grep start | egrep -o '([0-9]*)$')

    echo "Search string: $TABLE_NAME"
    PAGE_LIST=""

    # For every page in the PDF, find if it matches the table search string.
    for i in $(seq ${START_PAGE} ${PAGE_COUNT}); do
        # TODO: Only want to run pdf2txt once per page per job.
        PDF_LINES=$(pdf2txt.py -p ${i} "${PDF_FILE}")

        # Accumulate the matched pages and then pass them to python for extraction.
        RESULT=$(echo ${PDF_LINES} | egrep "${TABLE_NAME}")
        if [[ ${RESULT} ]]; then
            PAGE_LIST="${PAGE_LIST}${i},"
        fi
    done
    echo "Found on pages: ${PAGE_LIST:-None}"
    if [ ! -z ${PAGE_LIST} ]; then
        # Pass in a list of pages that match the table search string.
        python sureconnect.py ${CONFIG_FILE} ${PDF_FILE} "${TABLE_NAME}" ${PAGE_LIST} ${TEMPLATE} 
        PAGE_LIST=""
    fi
done

