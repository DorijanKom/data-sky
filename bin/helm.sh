#!/bin/bash

set -ueo pipefail

# Redirect fds so that output to &3 is real stdout, and &1 goes to stderr
# instead; this prevents accidentially intermixing with what helm sends to
# stdout.
exec 3>&1
exec 1>&2

# colors
RED='\033[0;31m'
#GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NOC='\033[0m'

# set your own options
MATCH_FILES_ARGS=".*secrets.y*"
DEC_SUFFIX=".dec"
COUNT_CHART_FAILED=0
COUNT_FILES_FAILED=0
COUNT_CHART=0
COUNT_FILES=0

CURRENT_COMMAND="${1:-}"

HELM_CMD="$(which helm)"

decrypt_helm_vars() {
    if [[ "$file" =~ $MATCH_FILES_ARGS ]]; then
        if [ -f "$file" ]; then
            echo -e "${YELLOW}>>>>>>${NOC} ${BLUE}Decrypt${NOC}"
            "$HELM_CMD" secrets dec "$file"
            (( ++COUNT_FILES ))
        else
            (( ++COUNT_FILES_FAILED ))
            return
        fi
    fi
}

function cleanup {
    case "${CURRENT_COMMAND}" in
        install|upgrade|rollback|template)
            echo -e "${YELLOW}>>>>>>${NOC} ${BLUE}Cleanup${NOC}"
            for file in "${@}"; do
                if [[ "$file" =~ $MATCH_FILES_ARGS ]]; then
                    "$HELM_CMD" secrets clean "${file}${DEC_SUFFIX}"
                fi
            done
    esac
}

function helm_cmd {
    echo ""
    $(echo "${HELM_CMD} $*" | sed -e 's/secrets.yaml/secrets.yaml.dec/g') >&3 || true
    local status=$?
    if [ "$status" -ne 0 ]; then
        echo ""
        cleanup "$@"
        exit 1
    else
        echo ""
        cleanup "$@"
        exit 0
    fi
}

case "${CURRENT_COMMAND}" in
    install|upgrade|rollback|template)
        for file in "$@"; do
            decrypt_helm_vars "$file"
        done
        ;;
esac

if [ "$COUNT_CHART" -eq 0 ] && [ "$COUNT_FILES" -eq 0 ] && [ "$COUNT_CHART_FAILED" -gt 0 ] && [ "$COUNT_FILES_FAILED" -gt 0 ];
then
    echo -e "${RED}Error no secrets found. No secret files in chart or secrets files defined${NOC}"
    exit 1
fi

# Run helm
helm_cmd "$@"
