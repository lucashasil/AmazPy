import os
import pytest
from unittest import mock
from amazpy.email import Email

@pytest.fixture
def email_credentials():
    return os.environ.get("AMAZPY_EMAIL_CREDENTIALS")

@pytest.fixture
def message():
    return "Test notification message"

@pytest.fixture
def email(email_credentials, message):
    return Email(email_credentials, message)

@pytest.fixture
def sender_email(email_credentials):
    return email_credentials.split(":")[0]

@pytest.fixture
def sender_password(email_credentials):
    return email_credentials.split(":")[1]

def test_email_subject(email):
    assert email.discount_message == "AmazPy: Product(s) you are tracking have dropped in price"

def test_email_init_success(email_credentials, message, sender_email, sender_password, capsys):
    with mock.patch("smtplib.SMTP") as mock_smtp:
        Email(email_credentials, message)
        captured = capsys.readouterr()
        assert "Email notification sent successfully!" in captured.out

        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_once_with(sender_email, sender_password)
        mock_smtp.return_value.sendmail.assert_called_once_with(
            sender_email, sender_email, mock.ANY
        )
        mock_smtp.return_value.quit.assert_called_once()

def test_email_init_failure(email_credentials, message, capsys):
    with mock.patch("smtplib.SMTP") as mock_smtp:
        # Simulate an exception during SMTP connection setup
        mock_smtp.side_effect = Exception("SMTP connection error")

        Email(email_credentials, message)
        captured = capsys.readouterr()
        assert "There was an issue sending a notification email" in captured.out

def test_send_email(email_credentials, message, sender_email):
    with mock.patch("smtplib.SMTP") as mock_smtp:
        email_instance = Email(email_credentials, message)
        email_instance.send_email(message)

        mock_smtp.return_value.sendmail.assert_called()
