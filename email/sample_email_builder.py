import smtplib

from email.mime.text import MIMEText
from email.utils import formatdate

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders

envelope_from = 'hello-ef@example.com'
rcpt_to = 'hello-rcpt@example.jp'

to_addr = 'hello-hdr@example.jp'
from_addr = 'hello-hdr@example.com'

def make_simple_part_email():
    envelope_from = 'hello@example.com'

    msg = MIMEText("テスト\n\nあいうえお")
    msg['Subject'] = 'タイトル'
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    return msg

def make_multi_part_email():

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

    return mime
