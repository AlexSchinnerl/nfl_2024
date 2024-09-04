import keyring
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MYMAIL = "alex.itsme@gmx.at"

my_intern_key = keyring.get_password("alxMail", "alex")

def send_weekly_mail(html_text, lastWeek, thisWeek):
    msg = MIMEMultipart()
    # -----Textbausteine
    msg["Subject"] = f"Ergebnisse Woche {lastWeek}, Tabelle Woche {thisWeek}"
    msg["From"] = MYMAIL
    msg.attach(MIMEText(f"Ergebnisse Woche {lastWeek}, Tabelle Woche {thisWeek}", "plain"))
    msg.attach(MIMEText(html_text, "html"))

    # --------Verbindung zu Server und wegschicken
    server = smtplib.SMTP("mail.gmx.net", 587)
    server.starttls()
    server.login(MYMAIL, my_intern_key)
    text = msg.as_string()
    server.sendmail(from_addr=MYMAIL, to_addrs="alexander.schinnerl@jku.at", msg=text)
    server.quit()
