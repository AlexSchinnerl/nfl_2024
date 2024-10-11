import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functions_key import MYKEY
# from email.mime.base import MIMEBase
# from email import encoders

MYMAIL = "alex.itsme@gmx.at"

def server_details(myMail, myKey, message):
    server = smtplib.SMTP("mail.gmx.net", 587)
    server.starttls()
    server.login(myMail, myKey)
    text = message.as_string()
    server.sendmail(from_addr=myMail, to_addrs="alex.itsme@gmx.at", msg=text)
    server.quit()

def send_mail_function(mailText, subject):

    msg = MIMEMultipart()
    # -----Textbausteine
    msg["Subject"] = subject
    msg["From"] = MYMAIL

    body = str(mailText) # der Mailtext
    msg.attach(MIMEText(body, "plain"))

    # --------Verbindung zu Server und wegschicken
    server = smtplib.SMTP("mail.gmx.net", 587)
    server.starttls()
    server.login(MYMAIL, MYKEY)
    text = msg.as_string()
    server.sendmail(from_addr=MYMAIL, to_addrs="alex.itsme@gmx.at", msg=text)
    server.quit()

# --------Attachement
# filename = "mail_text.txt"
# # attachment = open("mail_text.txt", "rb") 
# # Alternative:
# with open("mail_text.txt", "rb") as fp:
#     attachment = fp.read()

# p = MIMEBase("application", "octet-stream")
# p.set_payload((attachment).read())

# encoders.encode_base64(p)

# p.add_header("Content-Disposition", "attachment; filename= %s" % filename)

# msg.attach(p)

# # https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
# # https://codingworld.io/project/e-mails-versenden-mit-python