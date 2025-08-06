from sqlalchemy import Column, Integer
from database import Base

class Trajectory(Base):
    __tablename__ = "trajectory"
    id = Column(Integer, primary_key=True, index=True)
    x = Column(Integer)
    y = Column(Integer)
    step = Column(Integer)
