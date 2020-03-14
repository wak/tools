#!/usr/bin/python3

import smtplib
import sample_email_builder as builder

mailsv = 'localhost'
port = 10587

msg = builder.make_simple_part_email()
smtp = smtplib.SMTP(mailsv, port)
smtp.ehlo()
smtp.sendmail(builder.envelope_from, builder.to_addr, msg.as_string())
smtp.close()
