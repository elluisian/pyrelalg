#!/bin/bash

SCRIPT_DIR="$(dirname $(realpath ${BASH_SOURCE[0]}))"
if ! echo "$PYTHONPATH" | grep -q "$SCRIPT_DIR"
then
    export PYTHONPATH="$PYTHONPATH":"$SCRIPT_DIR"
fi
