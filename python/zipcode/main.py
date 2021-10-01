#! /usr/bin/env python3

import sys
import logging

import zipcode
from pprint import pprint

# a = zipcode.JapanPostZipcodeAddress('12345678', 'test1', 'a', '')
# b = zipcode.JapanPostZipcodeAddress('12345678', 'test1', 'b', '')
# pprint(a & b)
# exit()

logging.basicConfig(level=logging.DEBUG)
jpzipmap = zipcode.JapanPostZipcodeMap('ken_all.zip')

zipcode = sys.argv[1]
print(f'specified zip code: {zipcode}')
print('-- common --')
pprint(jpzipmap.find_common_address(zipcode))

print('\n-- all --')
pprint(jpzipmap.find_all_addresses(zipcode))
