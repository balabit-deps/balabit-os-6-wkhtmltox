#!/bin/bash
#
# Copyright (c) 2013-2016 BalaBit
# All Rights Reserved.
#

WKHTML_DIR=$(readlink -f ./)
docker run --rm -it -v $WKHTML_DIR:/wkhtmltox -e ZWA_SOURCE_DIR='/' wkhtmltox
