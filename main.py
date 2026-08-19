from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.ifc import PasswordHash
from pydantic import BaseModel
from typing  import Annotated

import models
from database import session_local
from schema import UpdateUser,Create_user,Note,NoteUpdate
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
async def get_user():
    pass

@app.post("/notes")
async def create_note(new:Note,session:db_Dep):
    new_note=models.Notes(new.title,new.content,new.date_created)
    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    return {"new note":new_note}


@app.put("/notes")
async def update_note(note_id:int,updated:NoteUpdate,session:db_Dep):
   fetched_note=session.get(Note,note_id)

   fetched_note.title=updated.title
   fetched_note.content=updated.content

@app.delete("/notes")
async def delete_note(note_id:int,session:db_Dep):
    fetched_note=session.get(Note,note_id)
    session.delete(fetched_note)
    session.refresh(fetched_note)

    return{"note deleted":"successfully"}