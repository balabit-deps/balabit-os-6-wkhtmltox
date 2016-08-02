#!/bin/bash
#
# Copyright (c) 2013-2016 BalaBit
# All Rights Reserved.
#

BUILD_PATH="static-build"

rm -rf "$BUILD_PATH"
scripts/build.py precise-amd64
chmod -R o+w "$BUILD_PATH"