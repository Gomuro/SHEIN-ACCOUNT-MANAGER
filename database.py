import uuid
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    uuid = Column(String, primary_key=True, default=str(uuid.uuid4()))
    account_name = Column(String, unique=True, nullable=False)
    proxy = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)
    cookies = Column(Text, nullable=False)


class Phone_emulator(Base):
    __tablename__ = 'phone_emulator'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    proxy = Column(String, nullable=False)
    avd_name = Column(String, nullable=False)
    account_name = Column(String, nullable=False)


engine = create_engine('sqlite:///accounts.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
