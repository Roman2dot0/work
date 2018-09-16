#! /usr/bin/env python3

import smtplib as smtp
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
import requests
import configparser
from datetime import date, timedelta


path = "settings.ini"
config = configparser.ConfigParser()
config.read(path)

hlogin = config.get("Settings", "hlogin")
hpass = config.get("Settings", "hpass")
url = config.get("Settings", "url")

f_date = date.strftime(date.today() - timedelta(days=3), ("%Y%m%d"))
h_filename = "bknProfi.{}.xlsx".format(f_date)
s_file = '{}.xlsx'.format(f_date)
http = url + h_filename

request = requests.get(http, auth=(hlogin, hpass))

with open(s_file, 'wb') as f:
    f.write(request.content)
f.close()


email = config.get("Settings", "email")
password = config.get("Settings", "password")
dest_email = config.get("Settings", "dest_email")
subject = "БД от Реалиста"
email_text = "В вложении"

message = MIMEMultipart()

part = MIMEBase('application', "octet-stream")
part.set_payload(open(s_file, "rb").read())
part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(s_file))
encoders.encode_base64(part)


message['From'] = email
message["To"] = dest_email
message["Subject"] = subject
message.attach(MIMEText(email_text))
message.attach(part)

server = smtp.SMTP_SSL('smtp.yandex.com')
server.ehlo(email)
server.login(email, password)
server.auth_plain()
server.sendmail(email, dest_email, message.as_bytes())
server.quit()
