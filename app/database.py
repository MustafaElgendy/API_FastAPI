from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


#SQLALCHEMY_DATABASE_URL = 'postgesql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' % quote_plus(settings.database_password)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush= False,bind= engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






# Connection to postgres database
# while True:
#     try:
#         conn = psycopg2.connect(host= 'localhost', database= 'fastapi',
#                                 user= 'postgres', password='m05t@f@1997', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Succesfully connected")
#         break
    
#     except Exception as error:
#         print("Connection failed")
#         print("Error: ", error)
#         time.sleep(2)