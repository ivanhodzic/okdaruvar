from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import smtplib
from email.mime.text import MIMEText

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def send_email(subject, message, to_email):
    email = 'ivanhodzic@gmail.com'
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = to_email

    # Gmail SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = email
    smtp_password = 'uuknvrerfmwwnlbx'

    # Start the SMTP connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Log in to the SMTP server
    server.login(smtp_username, smtp_password)

    # Send the email
    server.sendmail(email, to_email, msg.as_string())
   
    # Close the SMTP connection
    server.quit() 