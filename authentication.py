from fastapi import Depends, HTTPException

from jose import jwt,JWTError


from passlib.ifc import PasswordHash
from datetime import datetime, timezone, timedelta
from models import User
from sqlalchemy import select

from database   import db_Dep



from security import oauth2_scheme
SECRET_KEY="899782a10a58ef6e81bf49c3d8d3fc9705cc97144443068dd3a085ffb1dea4e6"
ALGORITHM="HS256"


def create_access_token(data:dict):
    token=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(hours=8)
    token.update({"exp":expire})
    encoded_jwt=jwt.encode(token,SECRET_KEY,algorithm=ALGORITHM)

    return  encoded_jwt


def get_current_user(session:db_Dep,token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401,detail="not found")

    user=session.execute(select(User).where(User.username==username)).scalars().first()
    if user is None:
        raise HTTPException(status_code=401,detail="not found")

    return user