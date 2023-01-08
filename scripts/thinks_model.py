from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship, backref,Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Think(Base):

    __tablename__ = "think_history"

    id = Column(Integer, primary_key=True,autoincrement=True)
    base_id = Column(Integer)
    base_text = Column(String)  
    balaboba_text = Column(String)  
    think_dt = Column(DateTime,server_default=func.now())  

    def __init__(self, base_text,balaboba_text,base_id=None):
        self.base_id = base_id    
        self.base_text = base_text    
        self.balaboba_text = balaboba_text