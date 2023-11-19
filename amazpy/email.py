import smtplib
from email.mime.text import MIMEText


class Email:
    def __init__(self, email_credentials: str, message: str):
        self.discount_message = "AmazPy: Product(s) you are tracking have dropped in price"
        self.email_credentials = email_credentials.split(":")
        try:
            self.s = smtplib.SMTP("smtp.gmail.com", 587)
            self.s.starttls()
            self.s.login(self.email_credentials[0], self.email_credentials[1])
            self.send_email(message)
        except:
            print("There was an issue sending a notification email, please check your credentials...")
            # Don't crash the script if a notification email fails to be sent
            pass

    def send_email(self, message):
        # Create a text/plain; charset="UTF-8" encoded email message
        email_message = MIMEText(message, "plain", "utf-8")

        # Set the subject and sender/receiver (the same) for the email
        email_message["Subject"] = self.discount_message
        email_message["From"] = self.email_credentials[0]
        email_message["To"] = self.email_credentials[0]

        # Send the email using the smtp server
        self.s.sendmail(self.email_credentials[0], self.email_credentials[0], email_message.as_string())

        # We are done with the smtp server for this email, so we can quit the connection
        # to ensure that it is tidied up correctly
        self.s.quit()
