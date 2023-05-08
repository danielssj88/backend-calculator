""" Module providing SQL Alchemy Models defition for the entities User, Operation and Record. """
from sqlalchemy import Column, Integer, Float, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """ User entity model. """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=20), unique=True, nullable=False)
    password = Column(String(length=100), nullable=False)
    status = Column(Enum('active', 'inactive'), nullable=False, default='active')

class Operation(Base):
    """ Operation entity model. """
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(length=20), unique=True, nullable=False)
    cost = Column(Float, nullable=False)

class Record(Base):
    """ Record entity model. """
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    operation_id = Column(Integer, ForeignKey('operations.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    user_balance = Column(Float, nullable=False)
    operation_response = Column(String(length=200))
    date = Column(DateTime, nullable=False)

    operation = relationship('Operation')
    user = relationship('User')
