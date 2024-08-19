import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

MYMAIL = "alex.itsme@gmx.at"

def send_mail_function(mail_key, mailText, subject):

    msg = MIMEMultipart()
    # -----Textbausteine
    msg["Subject"] = subject
    msg["From"] = MYMAIL
    # msg["To"] = MYMAIL #"alexander.schinnerl@jku.at"

    body = str(mailText) # der Mailtext
    msg.attach(MIMEText(body, "plain"))

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

    # --------Verbindung zu Server und wegschicken
    server = smtplib.SMTP("mail.gmx.net", 587)
    server.starttls()
    server.login(MYMAIL, mail_key)
    text = msg.as_string()
    server.sendmail(from_addr=MYMAIL, to_addrs="alexander.schinnerl@jku.at", msg=text)
    server.quit

# some_list = [1,2,3]

# send_mail_function(some_list)


# # https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/
# # https://codingworld.io/project/e-mails-versenden-mit-python