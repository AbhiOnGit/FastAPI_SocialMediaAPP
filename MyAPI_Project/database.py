import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import setting

# SQLALCHEMY_DATABASE_URL = "postgresql://<user name>:<password>@<ip-address/hostname>/<database name>
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Abhikeerti@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.DATABASE_USERNAME}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOSTNAME}:{setting.DATABASE_PORT}/{setting.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


# dependency vs
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
