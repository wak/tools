#! /usr/bin/env python3

import logging
import zipfile
import csv
import io
import collections

class JapanPostZipcodeMap(object):
    Address = collections.namedtuple('Address', 'address all')

    def __init__(self, ken_all_path):
        self._zipcode_map = dict()
        self._load_ken_all_zip(ken_all_path)

    def _load_ken_all_zip(self, ken_all_path):
        nr_rows = 0
        zip = zipfile.ZipFile(ken_all_path)
        with zip.open(zip.infolist()[0], 'r') as in_stream:
            with io.TextIOWrapper(in_stream, 'shift_jis_2004') as in_stream2:
                reader = csv.reader(in_stream2)
                for row in reader:
                    nr_rows += 1
                    self._register_address(
                        row[2],             # 3. 郵便番号(7桁)
                        JapanPostZipcodeAddress.from_raw_line(row)
                    )
        logging.info(f'Japan Post ZIP: %d rows found.', nr_rows)

    def _register_address(self, zipcode, address):
        self._zipcode_map.setdefault(zipcode, [])
        if address in self._zipcode_map[zipcode]:
            return

        self._zipcode_map[zipcode].append(address)

    def find_all_addresses(self, zipcode):
        if not zipcode in self._zipcode_map:
            return []
        return self._zipcode_map[zipcode]

    def find_common_address(self, zipcode):
        if not zipcode in self._zipcode_map:
            return None
        result = self._zipcode_map[zipcode][0]
        for address in self._zipcode_map[zipcode]:
            result &= address
        return result

class JapanPostZipcodeAddress(object):
    def __init__(self, zipcode, todofuken, shikuchoson, choiki):
        self.zipcode = zipcode
        self.todofuken = todofuken
        self.shikuchoson = shikuchoson
        self.choiki = choiki

    @classmethod
    def from_raw_line(cls, row):
        zipcode = row[2]        # 3. 郵便番号(7桁)
        todofuken = row[6]      # 7. 都道府県名
        shikuchoson = row[7]    # 8. 市区町村名
        choiki = row[8]         # 9. 町域名
        if choiki == '以下に掲載がない場合':
            choiki = ''
        return cls(zipcode, todofuken, shikuchoson, choiki)

    def address(self):
        return ''.join([self.todofuken, self.shikuchoson, self.choiki])

    def __eq__(self, other):
        if isinstance(other, JapanPostZipcodeAddress):
            return self.address() == other.address()
        return False

    def __and__(self, other):
        if self.zipcode != other.zipcode:
            raise Exception('zipcode should equal')

        todofuken = ''
        shikuchoson = ''
        choiki = ''
        if self.todofuken == other.todofuken:
            todofuken = self.todofuken
            if self.shikuchoson == other.shikuchoson:
                shikuchoson = self.shikuchoson
                if self.choiki == other.choiki:
                    choiki = self.choiki
        return JapanPostZipcodeAddress(self.zipcode, todofuken, shikuchoson, choiki)


    def __repr__(self):
        return f'<JapanPostZipcodeAddress {self.zipcode}, {self.todofuken}, {self.shikuchoson}, {self.choiki}>'
