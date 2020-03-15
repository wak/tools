#!/usr/bin/python3

import smtplib
import sample_email_builder as builder
import ssl

mailsv = 'localhost'
# mailsv = 'dummy-smtp.example.jp'

port = 10587

msg = builder.make_simple_part_email()
smtp = smtplib.SMTP(mailsv, port)
smtp.ehlo()

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations(cafile='keys/server.crt')
# context.load_verify_locations(cafile='keys/error-keys/server.crt')
smtp.starttls(context=context)

smtp.ehlo()
smtp.login('myid', 'mypass')
smtp.sendmail(builder.envelope_from, builder.to_addr, msg.as_string())
smtp.close()
