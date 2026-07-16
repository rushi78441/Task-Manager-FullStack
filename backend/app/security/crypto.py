import bcrypt
from datetime import datetime,timedelta,timezone
from app.config import settings
import jwt
from dotenv import load_dotenv
load_dotenv()
import os

def hash_password(password : str) -> str:
    """
    Convert Plain test password into a secure, non-reversible cryptographic hash
    """

    # generate a random salt value and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed.decode('utf-8')


def verify_password(plain_password : str, hashed_password : str) -> bool:
    """
    Verifies if an incoming plain-text password matches the stored hash.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


## JWT CONFIGS
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-for-testing-purposes-only")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES" , "30")

# create jwt token
def create_access_token(data : dict) -> str:
    """
    Generates a stateless JSON Web Token signed with our server's secret key.
    """
    to_encode = data.copy()

    # calculate the excat expiration timestamp in UTC
    expire = datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 'sub' (subject) represents the unique identifier, 'exp' represents the expiration claim
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, key = SECRET_KEY , algorithm = ALGORITHM)
    return encoded_jwt