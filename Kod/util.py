import string, secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_verification_code():
    alphabet = string.ascii_letters + string.digits
    verification_code = ''.join(secrets.choice(alphabet) for _ in range(6))
    return verification_code

def send_verification_email(email, code):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = ''
    smtp_password = ''

    sender_email = ''

    subject = 'TripPy - Your Verification Code'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject

    body = f'''
    Dear User,

    Your verification code is: {code}

    Regards,
    TripPy team
    '''

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, email, message.as_string())
        print("Verification email sent successfully.")
    except Exception as e:
        print("Error sending verification email:", str(e))


def send_reset_email(email, token):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = ''
    smtp_password = ''

    sender_email = 'm'

    subject = 'TripPy Password Reset Request'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject

    body = f'''
    Dear User,

    You have requested to reset your password. Please click the link below to reset your password:

    http://localhost:5000/reset_password/{token}

    If you did not request this, please ignore this email.

    Regards,
    TripPy team
    '''

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, email, message.as_string())
        print("Reset email sent successfully.")
    except Exception as e:
        print("Error sending reset email:", str(e))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}