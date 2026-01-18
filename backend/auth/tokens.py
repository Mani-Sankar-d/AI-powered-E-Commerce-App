# auth/tokens.py
import jwt
import os
from datetime import datetime, timedelta

def generate_access_token(user):
    payload = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    return jwt.encode(
        payload,
        os.getenv("ACCESS_TOKEN_SECRET"),
        algorithm="HS256"
    )

def generate_refresh_token(user):
    payload = {
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(
        payload,
        os.getenv("REFRESH_TOKEN_SECRET"),
        algorithm="HS256"
    )
