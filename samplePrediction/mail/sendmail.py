#!/bin/env python
# encoding:utf-8
#
# Author:   CORDEA
# Created:  2014-10-19
#

import smtplib
from email.mime.text import MIMEText

def sendMail(sub, msg, address):
    From    = "xxx@gmail.com"
    To      = address
    Subject = sub
    Message = msg

    msg  = MIMEText(Message)
    msg['Subject'] = Subject
    msg['From']    = From
    msg['To']      = To

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(From, "xxx")
    s.sendmail(From, To, msg.as_string())
    s.close()
