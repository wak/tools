#!/usr/bin/python3

import ssl
import smtplib

from email.mime.text import MIMEText
from email.utils import formatdate

mailsv = 'localhost'
port = 10587

envelope_from = 'hello@example.com'
to_addr = 'hello@example.jp'
from_addr = 'hello@example.jp'

msg = MIMEText("テスト\n\nあいうえお")
msg['Subject'] = 'タイトル'
msg['From'] = from_addr
msg['To'] = to_addr
msg['Date'] = formatdate()
print(msg)


smtp = smtplib.SMTP(mailsv, port)
smtp.ehlo()
smtp.sendmail(envelope_from, to_addr, msg.as_string())
smtp.close()
