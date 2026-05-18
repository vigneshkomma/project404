from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
import uuid
import bcrypt  

from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest

router = APIRouter()

# Config
SECRET_KEY = "CHNAGE_THIS_TO_ENV_SWCRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# Utils

def hash_password(password: str) -> str:
    """Encodes password to bytes, hashes it with a fresh salt, and decodes back to string."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    """Verifies a plain text password against the stored string hash."""
    return bcrypt.checkpw(
        plain.encode('utf-8'),
        hashed.encode('utf-8')
    )

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # python-jose expects a datetime object or int for 'exp'
    to_encode.update({"exp": expire}) 

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Sign-up
@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == payload.email).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        id = str(uuid.uuid4()),
        email = payload.email,
        username = payload.username,
        password_hash = hash_password(payload.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"user_id": new_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Login
@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }