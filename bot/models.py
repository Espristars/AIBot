from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Text, ForeignKey

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
    user_id = Column(BigInteger)
    username = Column(String, nullable=False)