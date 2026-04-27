from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)

    question = Column(String, nullable=False)
    answer = Column(String)

    status = Column(String, default="open", nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")   

    created_at = Column(DateTime, default=datetime.datetime.utcnow)