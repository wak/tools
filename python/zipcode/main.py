#! /usr/bin/env python3

import sys
import logging

import zipcode

logging.basicConfig(level=logging.DEBUG)
jpzipmap = zipcode.JapanPostZipcodeMap('ken_all.zip')

zipcode = sys.argv[1]
print(f'specified zip code: {zipcode}')
print(jpzipmap.get_address(zipcode))
