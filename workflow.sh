#!/usr/bin/env bash
#
# One of these objects per table expected in the PDF:
#
# [{
#   provider: ["auto" | "Sun Life" | "Manulife" | "London Life" | etc],
#   string_match: {
#       title_name: "by Number of Claims",
#       start_page: 14,
#       match_regex: "/.*/"
#   },
#   image_match: {
#       algo: "perceptual",
#       min_score: 48
#   },
#   extracts: {
#       flavour: ["lattice" | "stream"],
#       table_extractor: "my_table_extraction_fxn"
#   },
#   schema: "some_pandas_schema.filename",
#   schema: {
#       obj: "text"
#   },
#   fixups: {
#       TableShapeSchemaError: "my_dinrank_fixup"
#   },
#   template_map: {
#       src: "xyz",
#       dst: "abc"
#   }
# }]
#
# Only try the fixups once per parse attempt:
#
# conditions = {e: True for e in fixups}
# while (conditions.all())
#   try:
#       schema.validate(df)
#   except Exception as exception:
#     error_name = type(exception).__name__
#     if not conditions[error_name]:
#         logger.log('Already tried fixup! Failing!')
#         break
#     logger.log('Trying fixup!')
#     conditions[error_name] = fixups[error_name]()

# workflow.sh nfp_config.json 2020.pdf template.xlsm
CONFIG_FILE=${1}
PDF_FILE=${2}
TEMPLATE=${3}

# TODO: Get TABLE_NAME from CONFIG_FILE
TABLE_NAME=${CONFIG_FILE}

# `pdfinfo` on other platforms (`mdls` is macOS-specific)
PAGE_COUNT=$(mdls -raw -name kMDItemNumberOfPages "${PDF_FILE}")

PAGE_LIST=""

for i in $(seq ${PAGE_COUNT})
do
    PDF_LINES=$(pdf2txt.py -p ${i} "${PDF_FILE}")
    RESULT=$(echo ${PDF_LINES} | egrep "${TABLE_NAME}")
    if [[ ${RESULT} ]]; then
        PAGE_LIST="${PAGE_LIST}${i},"
    else
        python sureconnect.py ${CONFIG_FILE} ${PDF_FILE} ${TEMPLATE} ${PAGE_LIST} 
        PAGE_LIST=""
    fi
done
