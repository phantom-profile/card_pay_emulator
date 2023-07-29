import datetime
import uuid

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Uuid, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


SQLALCHEMY_DATABASE_URL = "sqlite:///./payments_service.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String, unique=True, index=True)
    token = Column(Uuid, default=uuid.uuid4)

    cards = relationship("Card", back_populates="trusted_app")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    card_number = Column(String, unique=True, index=True)
    cvv = Column(String, index=True)
    owner = Column(String)
    payment_system = Column(String)
    trusted_app_id = Column(Integer, ForeignKey("users.id"))

    trusted_app = relationship("User", back_populates="cards", foreign_keys=[trusted_app_id])
    sent_transactions = relationship("Transaction", back_populates="src", foreign_keys='Transaction.src_card_id')
    received_transactions = relationship("Transaction", back_populates="dst", foreign_keys='Transaction.dst_card_id')


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    src_card_id = Column(Uuid, ForeignKey("cards.id"), index=True)
    dst_card_id = Column(Uuid, ForeignKey("cards.id"), index=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    status = Column(String, index=True)
    amount_usd = Column(Float)

    src = relationship("Card", back_populates="sent_transactions", foreign_keys=[src_card_id])
    dst = relationship("Card", back_populates="received_transactions", foreign_keys=[dst_card_id])
