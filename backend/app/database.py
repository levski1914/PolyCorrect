from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL='postgresql://postgres.uwjgaqhmsvinsagqnxkg:asdf@aws-0-eu-central-1.pooler.supabase.com:5432/postgres'

engine= create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

metadata=MetaData()
Base=declarative_base()