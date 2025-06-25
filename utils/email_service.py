from flask_mail import Message
from app import mail
import os

def send_verification_email(user_email, token):
    verify_url = f"http://127.0.0.1:5000/auth/verify/{token}"
    msg = Message("Verify Your Account", sender=os.getenv("MAIL_USERNAME"), recipients=[user_email])
    msg.body = f"Click the link to verify your email: {verify_url}"
    mail.send(msg)
