from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from security import  pwd_context
from models import User,Notes
from schema import UpdateUser,Create_user,Note,NoteUpdate
from authentication import get_current_user, create_access_token
from database import db_Dep


app=FastAPI()


@app.get("/notes")
async def get_notes(session:db_Dep,current_user:User=Depends(get_current_user)):
    notes=session.get(Notes,current_user.owner_id)
    if not current_user:
        raise HTTPException(status_code=402, detail="forbidden")
    return notes

@app.post("/notes")
async def create_note(new:Note,session:db_Dep,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=402, detail="forbidden")
    new_note=Notes(new.title,new.content,new.date_created)
    session.add(new_note)
    session.commit()

    return {"new note":new_note}


@app.put("/notes")
async def update_note(updated:NoteUpdate,session:db_Dep,current_user:User=Depends(get_current_user)):
   if not current_user:
         raise HTTPException(status_code=402, detail="forbidden")
   fetched_note=session.get(Note,current_user.owner_id)
   fetched_note.title=updated.title
   fetched_note.content=updated.content
   session.commit()

   return {"updated":updated}

@app.delete("/notes")
async def delete_note(note_id:int,session:db_Dep,current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=402,detail="forbidden")
    fetched_note=session.get(Notes,note_id)
    session.delete(fetched_note)
    session.refresh(fetched_note)

    return{"note deleted":"successfully"}


#________user endpoints___________

@app.post("/user")
async def create_user(new_user:Create_user,session:db_Dep):
    user_new=User(username=new_user.username,
                  hashed_pwd=pwd_context.hash(new_user.password))
    existing=session.execute(select(User).where(User.username==user_new.username)).first()
    if existing:
        raise HTTPException(status_code=402,detail="bad request")
    session.add(user_new)
    session.commit()

    return {"new_user":user_new.username,
            "password":user_new.hashed_pwd}

@app.get("/user")
async def get_user(current_user:User=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=403,detail="forbidden")
    return current_user

@app.put("/user")
async def update_user(session:db_Dep,updated:UpdateUser,current_user:User=Depends(get_current_user)):
    fetched_user=session.get(User,current_user.owner_id)
    if fetched_user is None:
        raise  HTTPException(status_code=404,detail="could not be found")

    fetched_user.username=updated.username
    fetched_user.hashed_pwd=pwd_context.hash(updated.password)
    session.commit()
    session.refresh(fetched_user)

    return {"updated_user":updated}

@app.delete("/user")
async def delete_user(session:db_Dep,current_user:User=Depends(get_current_user)):
    user=session.get(User,current_user.owner_id)
    if user is None:
        raise HTTPException(status_code=404,detail="not found")
    session.delete(user)
    session.commit()
    session.refresh(user)

    return {"user":"deleted"}


@app.post("/login")
async def login(session:db_Dep,form_data:OAuth2PasswordRequestForm=Depends()):
    user=session.execute(select(User).where(User.username==form_data.username)).first()
    if user is None:
        raise HTTPException(404,"not found")
    verif=pwd_context.verify(form_data.password,user.hashed_password)
    if not verif:
        raise HTTPException(401,"unauthorized")
    access_token=create_access_token(data={"sub":user.username})

    return {"access_token":access_token,
            "token_type":"bearer"}




