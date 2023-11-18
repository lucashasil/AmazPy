import smtplib


class Email:
    def __init__(self, email_credentials: str, message: str):
        self.email_credentials = email_credentials.split(":")
        self.s = smtplib.SMTP("smtp.gmail.com", 587)
        self.s.starttls()
        self.s.login(self.email_credentials[0], self.email_credentials[1])
        self.send_email(message)

    def send_email(self, message):
        self.s.sendmail(self.email_credentials[0], self.email_credentials[0], message)
        self.s.quit()
