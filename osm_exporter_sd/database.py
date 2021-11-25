from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import settings

__connect_args = {}
if settings.db_url.startswith("sqlite://"):
    __connect_args["check_same_thread"] = False

engine = create_engine(settings.db_url, connect_args=__connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
