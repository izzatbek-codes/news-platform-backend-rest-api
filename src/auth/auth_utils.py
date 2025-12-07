from passlib.context import CryptContext
from src.models.users_model import Users
from fastapi import status, HTTPException
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, status


pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')
SECRET_KEY = '08fc99681c4ba63c59236c5637c75c2e06ce67dd924c8d57e326cb563d8426b3'
ALGORITHM = 'HS256'
oauth_bearer = OAuth2PasswordBearer(tokenUrl='/auth/login')


def authenticate_user(email, password, db):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')
    return user


def create_access_token(email: str, id: int, role: str, expire_delta: timedelta):
    encode = {'email': email, 'id': id, 'role': role}
    expire = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get('email')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if not user_email or not user_role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
        return {'email': user_email, 'id': user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
        
USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]


