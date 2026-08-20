from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing  import Annotated

from sqlalchemy import select

from auth import oauth2_scheme, pwd_context
from models import User,Notes
from database import session_local
from schema import UpdateUser,Create_user,Note,NoteUpdate
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from auth import get_current_user



app=FastAPI()


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
    new_note=Notes(new.title,new.content,new.date_created)
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


#________user endpoints___________

@app.post("/user")
async def create_user(new_user:Create_user,session:db_Dep):
    user_new=User(username=new_user.username,
                         password=pwd_context.hash(new_user.password))
    existing=session.execute(select(User).where(User.username==user_new.username)).first()
    if existing:
        raise HTTPException(status_code=402,detail="bad request")
    session.add(user_new)
    session.commit()
    session.refresh(user_new)

@app.get("/user")
async def get_user(current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=403,detail="forbidden")
    return current_user

@app.put("/user")
async def update_user(session:db_Dep,updated:UpdateUser,current_user:User=Depends(get_current_user)):
    fetched_user=session.get(User,current_user.owner_id)
    if fetched_user is None:
        raise  HTTPException(status_code=401,detail="could not be found")

    fetched_user.username=updated.username
    fetched_user.hashed_pwd=pwd_context.hash(updated.pwd)


