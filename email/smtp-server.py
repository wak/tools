#! /usr/bin/env python3

import os
import re
import configparser

import smtpd
import asyncore

import email.parser
import quopri

import smtplib

from pprint import pprint
import traceback

class MySMTPServer(smtpd.SMTPServer):
    def __init__(self, local_tuple, config):
        super().__init__(local_tuple, None)
        self._config = config
    
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        try:
            pprint(rcpttos)
            MessageInspector.inspect_from_bytes(mailfrom, rcpttos, data)
            if self._config.relay_email:
                self._relay_to_office365(mailfrom, rcpttos, data)
        except Exception as e:
            traceback.print_exc()

    def _overwrite_sender(self, data):
        msg = email.message_from_bytes(data)
        if msg['From'] != self._config.smtp_auth_id:
            print('overwrite From header %s => %s' % (msg['From'], self._config.smtp_auth_id))
            msg['From'] = self._config.smtp_auth_id

        return msg.as_string()

    def _relay_to_office365(self, mailfrom, rcpttos, data):
        smtp = smtplib.SMTP('smtp.office365.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self._config.smtp_auth_id, self._config.smtp_auth_password)
        smtp.ehlo()
        smtp.sendmail(self._config.smtp_auth_id, rcpttos, self._overwrite_sender(data))
        smtp.close()

        print('Relay ... OK.')

class MessageInspector(object):
    def __init__(self, envelope_from, rcpt_tos, message):
        self._envelope_from = envelope_from
        self._rcpt_tos = rcpt_tos
        self._message = message
    
    @staticmethod
    def inspect_from_bytes(envelope_from, rcpt_tos, message_bytes):
        msg = email.message_from_bytes(message_bytes)
        MessageInspector(envelope_from, rcpt_tos, msg).inspect()

    def inspect(self):
        print("=" * 80)

        self._inspect_envelope_from()
        self._inspect_rcpt_tos()
        self._inspect_headers()
        
        if self._message.is_multipart():
            self._inspect_multi_part()
        else:
            self._inspect_single_part()

        print("=" * 80)

    def _inspect_envelope_from(self):
        print("[%s]\n  %s" % ('Envelope From', self._envelope_from))

    def _inspect_rcpt_tos(self):
        print("[RCPT TO]")
        for rcpt_to in self._rcpt_tos:
            print("  %s" % (rcpt_to))
        
    def _inspect_headers(self):
        print("[HEADERS]")
        for key, value in self._message.items():
            print("  %-25s: %s" % (key, self._decode_header(value)))

    def _inspect_multi_part(self):
        for payload in self._message.get_payload():
            charset = payload.get_content_charset()
            if payload.get_filename() is None:
                print("[BODY]")
                body = payload.get_payload(None, True).decode(charset or 'utf-8')
                print(re.sub(r'^', "  ", body, flags=re.MULTILINE))
            else:
                print("[Attachment] ", self._decode_header(payload.get_filename()))

    def _inspect_single_part(self):
        print("[BODY]")
        charset = self._message.get_content_charset()
        body = self._message.get_payload(None, True).decode(charset or 'utf-8')
        print(re.sub(r'^', "  ", body, flags=re.MULTILINE))

    def _decode_header(self, header_value):
        return ''.join([v if type(v) is str else v.decode(cset or 'utf-8')
                        for (v, cset) in email.header.decode_header(header_value)])

class Config(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'smtp-server.conf'))

        with open(config_file) as f:
            config.read_file(f)

        section = config['smtp-server']
        self.relay_email = section.getboolean('RELAY_EMAIL', False)
        self.smtp_auth_id = section.get('SMTP_AUTH_ID')
        self.smtp_auth_password = section.get('SMTP_AUTH_PASSWORD', '')

        # self.dump()

    def dump(self):
        print('[CONFIG]')
        print('  Relay: ' + str(self.relay_email))
        print('  ID   : ' + self.smtp_auth_id)
        print('  Pass : ' + self.smtp_auth_password)

def main():
    try:
        config = Config()
        sv = MySMTPServer(('localhost', 10587), config)
        print("Dummy SMTP Server started.")
        asyncore.loop()
    except KeyboardInterrupt:
        pass

main()
