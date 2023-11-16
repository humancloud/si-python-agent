#!/bin/sh

#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

# get tests from both unit and plugin
declare -a unit_tests=( $(ls -d tests/unit ) )

declare -a plugin_tests=( $(ls -d tests/plugin/{data,http,web} | grep -v '__pycache__' ))

dest=( "${unit_tests[@]}" "${plugin_tests[@]}" )

printf '%s\n' "${dest[@]}" | jq -R . | jq -cs .
