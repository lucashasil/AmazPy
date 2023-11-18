import smtplib
from email.mime.text import MIMEText


class Email:
    def __init__(self, email_credentials: str, message: str):
        self.discount_message = "AmazPy: Product(s) you are tracking have dropped in price"
        self.email_credentials = email_credentials.split(":")
        self.s = smtplib.SMTP("smtp.gmail.com", 587)
        self.s.starttls()
        self.s.login(self.email_credentials[0], self.email_credentials[1])
        self.send_email(message)

    def send_email(self, message):
        email_message = MIMEText(message, "plain", "utf-8")
        email_message["Subject"] = self.discount_message
        email_message["From"] = self.email_credentials[0]
        email_message["To"] = self.email_credentials[0]
        self.s.sendmail(self.email_credentials[0], self.email_credentials[0], email_message.as_string())
        self.s.quit()
