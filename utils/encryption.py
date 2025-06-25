from itsdangerous import URLSafeTimedSerializer
import os

SECRET_KEY = os.getenv("SECRET_KEY")
serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_token(email):
    return serializer.dumps(email, salt="email-confirm")

def verify_token(token, max_age=3600):
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=max_age)
        return email
    except:
        return None
