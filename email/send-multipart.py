#!/usr/bin/python3

import ssl
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email.header import Header
from email import encoders

mailsv = 'localhost'
port = 10587

envelope_from = 'hello-ef@example.com'
rcpt_to = 'hello-rcpt@example.jp'

to_addr = 'hello-hdr@example.jp'
from_addr = 'hello-hdr@example.com'

body = "テスト\n\nあいうえお"

mime = MIMEMultipart()
mesg = MIMEText(_text=body, _subtype='plain', _charset='utf-8')
mime.attach(mesg)

mime['Subject'] = 'My Subject'
mime['From'] = from_addr
mime['To'] = to_addr
mime['Date'] = formatdate(localtime=True)

part = MIMEBase('plain', 'text')
part.set_payload('ファイルの中身')
encoders.encode_base64(part)
attach_filename = Header('添付ファイル1.txt', 'utf-8').encode()
part.set_param('name', attach_filename)
part.add_header("Content-Disposition", "attachment", filename=attach_filename)
mime.attach(part)


part = MIMEBase('plain', 'text')
part.set_payload('file contents')
encoders.encode_base64(part)
attach_filename = Header('attachment-file2.txt', 'utf-8').encode()
part.set_param('name', attach_filename)
part.add_header("Content-Disposition", "attachment", filename=attach_filename)
mime.attach(part)

smtp = smtplib.SMTP(mailsv, port)
smtp.ehlo()
smtp.sendmail(envelope_from, rcpt_to, mime.as_string())
smtp.close()
