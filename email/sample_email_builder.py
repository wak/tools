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
    msg = MIMEText("テスト\n\nあいうえお")
    msg['Subject'] = 'タイトル'
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    return msg

def make_english_email():
    msg = MIMEText("English Email")
    msg['Subject'] = 'My Subject'
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    return msg

def make_iso_2022_jp_charset_email():
    msg = MIMEText("ISO-20220-JP\nで作られた本文。", _charset="iso-2022-jp")
    msg['Subject'] = Header('ISO-2022-JPのタイトル', "iso-2022-jp").encode()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    return msg

def make_multi_part_email():
    body = "添付ファイルが2個ついているメール"

    mime = MIMEMultipart()
    mesg = MIMEText(_text=body, _subtype='plain', _charset='utf-8')
    mime.attach(mesg)

    mime['Subject'] = 'マルチパートのメール'
    mime['From'] = from_addr
    mime['To'] = to_addr
    mime['Date'] = formatdate(localtime=True)

    mime.attach(_attachment('日本語ファイル.txt', 'utf-8', 'ファイルの中身'))
    mime.attach(_attachment('english-file.txt', 'utf-8', 'file contents'))

    return mime

def _attachment(file_name, file_name_charset, payload):
    part = MIMEBase('plain', 'text')
    part.set_payload(payload)
    encoders.encode_base64(part)
    
    filename = Header(file_name, file_name_charset).encode()
    part.set_param('name', filename)
    part.add_header("Content-Disposition", "attachment", filename=filename)

    return part
