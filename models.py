from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

class Base(declarative_base):
    pass

class questions(Base):
    __tablename__="questions"
    question_id=Column(Integer,primary_key=True,index=True)
    question_text=Column(String,index=True)

class choices(Base):
    choice_id=Column(Integer,primary_key=True,index=True)
    choice_text=Column(Integer,index=True)
    question_id=Column(Integer,ForeignKey("question_id"),index=True)