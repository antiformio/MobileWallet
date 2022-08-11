from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    db_username = Column(String)
    db_password = Column(String)

    wallet = relationship(
        "Wallet", backref="user", uselist=False
    )  # uselist to define one-to-one


class Wallet(Base):
    __tablename__ = "wallet"
    id = Column(Integer, primary_key=True)
    balance = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    transactions = relationship("Transaction")


class TransactionConcepts(str, Enum):
    outgoing = "OUTGOING"
    incoming = "INCOMING"


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey("wallet.id"))
    to_user = Column(Integer)
    from_user = Column(Integer)
    amount = Column(Integer)
    concept = Column(String)
    description = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
