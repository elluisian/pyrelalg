#!/bin/bash

D="$(dirname $(realpath ${BASH_SOURCE[0]}))"
export PYTHONPATH="$PYTHONPATH":"$D"
