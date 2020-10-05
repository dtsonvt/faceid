# -*- coding: utf-8 -*-
import asyncio
import aiosmtplib
import sys
from static.functions import logger
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from os.path import basename

MAIL_PARAMS = {
    "TLS": True,
    "host": "smtp.gmail.com",
    "password": "Th@ison@123456",
    "user": "IPC247Mail@gmail.com",
    "port": 587,
}

if sys.platform == "win32":
    loop = asyncio.get_event_loop()
    if not loop.is_running() and not isinstance(loop, asyncio.ProactorEventLoop):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)


async def send_mail_async(to, subject, text, textType="plain", **params):
    try:

        cc = params.get("cc", [])
        bcc = params.get("bcc", [])
        mail_params = params.get("mail_params", MAIL_PARAMS)
        # Prepare Message
        msg = MIMEMultipart("related")
        msg.preamble = "Dear Mr./Mrs."
        msg["Subject"] = subject
        msg["From"] = mail_params.get("user", "IPC247Mail@gmail.com")
        msg["To"] = ", ".join(to)

        # msgAlternative = MIMEMultipart("alternative")
        # msg.attach(msgAlternative)

        if len(cc):
            msg["Cc"] = ", ".join(cc)
        if len(bcc):
            msg["Bcc"] = ", ".join(bcc)

        msg.attach(MIMEText(text, textType))

        # attch file
        # This example assumes the image is in the current directory
        # fp = open("error2.jpg", "rb")
        # msgImage = MIMEImage(fp.read())
        # fp.close()
        # msgImage.add_header("Content-ID", "<image1>")
        # msg.attach(msgImage)

        # Contact SMTP server and send Message
        host = mail_params.get("host", "localhost")
        isSSL = mail_params.get("SSL", False)
        isTLS = mail_params.get("TLS", False)
        port = mail_params.get("port", 465 if isSSL else 25)
        smtp = aiosmtplib.SMTP(hostname=host, port=port, use_tls=isSSL)
        await smtp.connect()
        if isTLS:
            await smtp.starttls()
        if "user" in mail_params:
            await smtp.login(mail_params["user"], mail_params["password"])
        await smtp.send_message(msg)
        await smtp.quit()
        return True
    except Exception as ex:
        logger.error("end send_mail_async: \nERROR: {}".format(ex))
        return False
