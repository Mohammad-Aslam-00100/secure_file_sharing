import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

payload = {
    "role": "ops"
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print("Use this token in Postman:\n")
print(token)
