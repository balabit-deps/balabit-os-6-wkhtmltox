#!/bin/bash
#
# Copyright (c) 2013-2016 BalaBit
# All Rights Reserved.
#

docker rmi wkhtmltox
cp ./debian/control ./tests/environment/
docker build -t wkhtmltox  ./tests/environment
rm tests/environment/control
