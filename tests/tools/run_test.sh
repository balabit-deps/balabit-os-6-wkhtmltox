#!/bin/bash
#
# Copyright (c) 2013-2016 BalaBit
# All Rights Reserved.
#

# build wkhtml before run tests
sh ./tests/tools/build.sh
echo
echo "Running tests..."

TEST_PATH="tests/reporting"
RESULTS_PATH="$TEST_PATH/results"

rm -rf "$RESULTS_PATH"

nosetests3 -v --nocapture "$TEST_PATH"
return_code=$?

if [ -d "$RESULTS_PATH" ]; then
  chmod -R o+w "$RESULTS_PATH"
fi

exit "$return_code"
