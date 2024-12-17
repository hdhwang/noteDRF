import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.format_helper import *

logger = logging.getLogger(__name__)


def smtp_relay(email_msg):
    msg = ""
    contents = MIMEMultipart()

    try:
        server = smtplib.SMTP("sendmail")

        from_addr = email_msg.get("From")
        to_addrs = email_msg.get("To") + email_msg.get("Cc") + email_msg.get("Bcc")

        if email_msg.get("From"):
            from_msg = ",".join(email_msg.get("From"))
            msg += f"From: {from_msg}\r\n"

        if email_msg.get("To"):
            to_msg = ",".join(email_msg.get("To"))
            msg += f"To: {to_msg}\r\n"

        if email_msg.get("Cc"):
            cc_msg = ",".join(email_msg.get("Cc"))
            msg += f"CC: {cc_msg}\r\n"

        if email_msg.get("Subject"):
            subject_msg = email_msg.get("Subject")
            contents["Subject"] = f"{subject_msg}\r\n\r\n"

        if email_msg.get("Msg"):
            contents.attach(MIMEText(email_msg.get("Msg"), "html"))

        msg += contents.as_string()

        server.sendmail(from_addr=from_addr, to_addrs=to_addrs, msg=msg)
        server.quit()

    except Exception as e:
        logger.warning(f"[smtp_relay] {to_str(e)}")


def send_mail(mail_from, mail_to, mail_cc, mail_bcc, subject, msg):
    try:
        email_msg = {
            "Subject": subject,
            "From": mail_from,
            "To": mail_to,
            "Cc": mail_cc,
            "Bcc": mail_bcc,
            "Msg": msg,
        }
        smtp_relay(email_msg)

    except Exception as e:
        logger.warning(f"[send_mail] {to_str(e)}")


# html style 조회
def get_html_style():
    return (
        "<style>body { background: #fff; }"
        ".bluetop {border-collapse: collapse;border-top: 3px solid #168;}"
        ".bluetop th {color: #168;background: #f0f6f9;}"
        ".bluetop th, .bluetop td {padding: 10px;border: 1px solid #ddd;}"
        ".bluetop th:first-child, .bluetop td:first-child {border-left: 0;}"
        ".bluetop th:last-child, .bluetop td:last-child {border-right: 0;}</style>"
    )
