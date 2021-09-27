#! /usr/bin/env python3

import logging
import zipfile
import csv
import io
import collections

class JapanPostZipcodeAddress(object):
    def __init__(self, row):
        self.zipcode = row[2]        # 3. 郵便番号(7桁)
        self.todofuken = row[6]      # 7. 都道府県名
        self.shikuchoson = row[7]    # 8. 市区町村名
        self.choiki = row[8]         # 9. 町域名
        if self.choiki == '以下に掲載がない場合':
            self.choiki = ''

    def values(self):
        return [self.todofuken, self.shikuchoson, self.choiki]

    def address(self):
        return ''.join(self.values())

    def __eq__(self, other):
        if isinstance(other, JapanPostZipcodeAddress):
            return self.address() == other.address()
        return False

class JapanPostZipcodeMap(object):
    Address = collections.namedtuple('Address', 'address all')

    def __init__(self, ken_all_path):
        self._zipcode_map = dict()

        nr_rows = 0
        zip = zipfile.ZipFile(ken_all_path)
        with zip.open(zip.infolist()[0], 'r') as in_stream:
            with io.TextIOWrapper(in_stream, 'shift_jis_2004') as in_stream2:
                reader = csv.reader(in_stream2)
                for row in reader:
                    self._process_zip_csv_row(row)
                    nr_rows += 1
        logging.info(f'Japan Post ZIP: %d rows found.', nr_rows)

    def _process_zip_csv_row(self, row):
        self._register_address(
            row[2],             # 3. 郵便番号(7桁)
            JapanPostZipcodeAddress(row)
        )

    def _register_address(self, zipcode, address):
        if zipcode in self._zipcode_map:
            if address in self._zipcode_map[zipcode]:
                # logging.info('duplicated zip address: %s', repr(all_data))
                pass
            else:
                self._zipcode_map[zipcode].append(address)
        else:
            self._zipcode_map[zipcode] = [address]

    def get_addresses(self, zipcode):
        if not zipcode in self._zipcode_map:
            return []
        return self._zipcode_map[zipcode]

    def get_address(self, zipcode):
        return self._get_common_address(self.get_addresses(zipcode))

    def _get_common_address(self, addresses):
        if not addresses:
            return []

        for i in range(3):
            compareing = addresses[0].values()[i]
            for a in addresses:
                if compareing != a.values()[i]:
                    return ''.join(a.values()[0:i])
        return a.address()
