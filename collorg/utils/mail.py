#!/usr/bin/python
#-*- coding: utf-8 -*-

import smtplib

from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
import cStringIO
import base64
import email.Message
import email.Utils
import mimetypes
import quopri

class Mail():
    def __init__(self, db):
        self.db = db
        self.__smtp_server = db._cog_params['smtp_server']
        self.__email = MIMEMultipart('alternative')

    def set_from(self, from_):
        self.__from = from_
        self.__email['From'] = from_
        self.__email['Sender'] = from_

    def set_to(self, to):
        self.__to = to
        self.__email['To'] = ",".join(to)

    def set_cc(self, cc_):
        self.__email['Cc'] = ','.join(cc_)

    def set_bcc(self, bcc_):
        self.__email['Bcc'] = ",".join(bcc_)

    def set_subject(self, subject):
        self.__email['Subject'] = subject

    def set_body(self, text, _subtype = 'plain', _charset = "utf-8"):
        self.__email.attach(MIMEText(text, _subtype, _charset))

    def send(self):
#        open("/tmp/cog_mail", "a+").write("sending: {}->{}\n{}\n".format(
#            self.__from, self.__to, self.__email.as_string()))
        smtp = smtplib.SMTP(self.__smtp_server)
        smtp.sendmail(
            self.__from,
            self.__to,
            self.__email.as_string() )
        smtp.quit()

    def attach(self, chemin_fichier):
        raise NotImplementedError
        fileName = chemin_fichier.split( '/' )[-1]
        contentType,ignored=mimetypes.guess_type(fileName)
        if contentType==None: # If no guess, use generic opaque type
          contentType="application/octet-stream"
        contentsEncoded=cStringIO.StringIO()
        f=open(chemin_fichier,"rb")
        mainType=contentType[:contentType.find("/")]
        if mainType=="text":
          cte="quoted-printable"
          quopri.encode(f,contentsEncoded,1) # 1 for encode tabs
        else:
          cte="base64"
          base64.encode(f,contentsEncoded)
        f.close()
        subMsg=email.Message.Message()
        subMsg.add_header("Content-type",contentType,name=fileName)
        subMsg.add_header("Content-transfer-encoding",cte)
        subMsg.set_payload(contentsEncoded.getvalue())
        contentsEncoded.close()
        self.__email.attach( subMsg )
