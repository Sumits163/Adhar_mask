from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import contextlib

engine = create_engine("sqlite:///app.db", echo=True)

def get_db_session():
    return Session(engine)