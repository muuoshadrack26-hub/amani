from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
database_url="postgresql://amani:amani55@localhost:5432/amani"
engine=create_engine(database_url)

session_local=sessionmaker()

