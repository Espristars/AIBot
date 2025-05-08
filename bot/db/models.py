from time import timezone

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('clients.user_id'))
    role = Column(String)
    content = Column(Text)

class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String, nullable=False)
    last_model = Column(String, nullable=False)
    last_mode = Column(String, nullable=False, server_default="friendly")
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    subscription_type = Column(String, nullable=False, server_default="start")
    subscription_end_date = Column(DateTime(timezone=True))