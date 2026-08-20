from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import psycopg2
database_url="postgresql://amani:amani55@localhost:5432/amani"
engine=create_engine(database_url)

session_local=sessionmaker(autocommit=False,autoflush=False,bind=engine)

async def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()


db_Dep=Annotated [Session,Depends(get_db)]