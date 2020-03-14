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
        smtp_server.MessageInspector.inspect_from_bytes('test@example.com', ['test@example.com'], mail.as_bytes())

if __name__ == "__main__":
    unittest.main()
