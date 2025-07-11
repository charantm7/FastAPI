
from sqlalchemy import create_engine
from sqlalchemy .ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

postgresql_user = os.getenv("postgresql_user")
postgresql_password = os.getenv("postgresql_password")
hostname = os.getenv("hostname")
db_name = os.getenv("db_name")

SQLALCHEMY_DATABASE_URL = (f'postgresql://{postgresql_user}:{postgresql_password}@{hostname}/{db_name}')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionlocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)

Base = declarative_base()

    
def get_db():
    db = sessionlocal() #creates a session with sqlachemy
    try:
        yield db #temp handover the session to fastapi

    finally:
        db.close() #if anything goes wrong it closes the db





