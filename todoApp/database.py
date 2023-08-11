from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL='postgresql://yywefbyg:yeE44FtB6enLV3Sst18wtOjMgnxmHICF@otto.db.elephantsql.com/yywefbyg'



engine=create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()
