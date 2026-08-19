from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.ifc import PasswordHash
from pydantic import BaseModel
from typing  import Annotated
from database import session_local
import schema
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY="899782a10a58ef6e81bf49c3d8d3fc9705cc97144443068dd3a085ffb1dea4e6"
ALGORITHM="HS256"


app=FastAPI()
amani="words"
muuo=pwd_context.hash(amani)
#print(muuo)

async def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()

db_Dep=Annotated [Session,Depends(get_db)]


@app.get("/notes")
async def create_note
