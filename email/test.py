#!/usr/bin/env python3

import unittest
import sample_email_builder as builder
import smtp_server

class TestMessageInspector(unittest.TestCase):
    def test_simple_part_email(self):
        mail = builder.make_simple_part_email()
        smtp_server.MessageInspector.inspect_from_bytes('test@example.com', ['test@example.com'], mail.as_bytes())

    def test_multi_part_email(self):
        mail = builder.make_multi_part_email()
        self._inspect(mail)

    def test_no_charset_email(self):
        mail = builder.make_english_email()
        self._inspect(mail)

    def test_iso_2022_jp(self):
        mail = builder.make_iso_2022_jp_charset_email()
        self._inspect(mail)

    def _inspect(self, mail):
        data = mail.as_bytes()
        smtp_server.MessageInspector.inspect_from_bytes('test@example.com', ['test@example.com'], data)

if __name__ == "__main__":
    unittest.main()
