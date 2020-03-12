#! /usr/bin/env python3

## 設定 ##########################
# メールを転送する？
RELAY_EMAIL = False

# SMTP認証ID
MAIL_ADDRESS = ''

# SMTP認証パスワード
MAIL_PASSWORD = ''
##################################

import smtpd
import asyncore

import email.parser
import quopri

import ssl
import smtplib

import re

from pprint import pprint
import traceback

class MySMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        try:
            self._describe_email(peer, mailfrom, rcpttos, data, **kwargs)
            if RELAY_EMAIL:
                self._relay_to_office365(mailfrom, rcpttos, data)
        except Exception as e:
            traceback.print_exc()
    
    def _describe_email(self, peer, mailfrom, rcpttos, data, **kwargs):
        print("=" * 80)
        print("[%s]\n  %s" % ('Envelope From', mailfrom))

        print("[HEADERS]")
        msg = email.message_from_bytes(data)
        for key, value in msg.items():
            print("  %-25s: %s" % (key, self._decode_header(value)))

        if msg.is_multipart():
            for payload in msg.get_payload():
                charset = payload.get_content_charset()
                if payload.get_filename() is None:
                    print("[BODY]")
                    body = payload.get_payload(None, True).decode(charset)
                    print(re.sub(r'^', "  ", body, flags=re.MULTILINE))
                else:
                    print("[Attachment] ", self._decode_header(payload.get_filename()))
        else:
            print("[BODY]")
            charset = msg.get_content_charset()
            body = msg.get_payload(None, True).decode(charset)
            print(re.sub(r'^', "  ", body, flags=re.MULTILINE))

        print("=" * 80)

    def _decode_header(self, header_value):
        return ''.join([v if type(v) is str else v.decode(cset) for (v, cset) in email.header.decode_header(header_value)])


    def _overwrite_sender(self, data):
        msg = email.message_from_bytes(data)
        if msg['From'] != MAIL_ADDRESS:
            print('overwrite From header %s => %s' % (msg['From'], MAIL_ADDRESS))
            msg['From'] = MAIL_ADDRESS

        return msg.as_string()

    def _relay_to_office365(self, mailfrom, rcpttos, data):
        smtp = smtplib.SMTP('smtp.office365.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(MAIL_ADDRESS, MAIL_PASSWORD)
        smtp.ehlo()
        smtp.sendmail(MAIL_ADDRESS, rcpttos, self._overwrite_sender(data))
        smtp.close()

        print('Relay ... OK.')

def main():
    sv = MySMTPServer(('localhost', 10025), None)
    asyncore.loop()

main()
