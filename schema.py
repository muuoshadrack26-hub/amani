from pydantic import BaseModel
from datetime import datetime

class Note(BaseModel):
    note_id:int
    title:str
    content:str
    date_created:datetime

class NoteUpdate(BaseModel):
    title:str
    content:str


class Create_user(BaseModel):
    user_id:int
    username:str
    password:str

class UpdateUser(BaseModel):
    username:str
    password:str

