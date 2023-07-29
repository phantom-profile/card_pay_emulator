import datetime
import uuid

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Uuid, DateTime, Float, UniqueConstraint
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

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    app_name = Column(String, unique=True, index=True, nullable=False)
    token = Column(Uuid, default=uuid.uuid4, nullable=False)

    cards = relationship("Card", back_populates="trusted_app")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4, nullable=False)
    card_number = Column(String, unique=True, index=True, nullable=False)
    cvv = Column(String, index=True, nullable=False)
    owner = Column(String, nullable=False)
    payment_system = Column(String, nullable=False)
    trusted_app_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_name = Column(String, nullable=False)

    trusted_app = relationship("User", back_populates="cards", foreign_keys=[trusted_app_id])
    sent_transactions = relationship("Transaction", back_populates="src", foreign_keys='Transaction.src_card_id')
    received_transactions = relationship("Transaction", back_populates="dst", foreign_keys='Transaction.dst_card_id')

    __table_args__ = (UniqueConstraint('card_number', 'cvv', name='card_number_cvv_index'),)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    src_card_id = Column(Uuid, ForeignKey("cards.id"), index=True, nullable=False)
    dst_card_id = Column(Uuid, ForeignKey("cards.id"), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    status = Column(String, index=True, nullable=False)
    amount_usd = Column(Float, nullable=False)

    src = relationship("Card", back_populates="sent_transactions", foreign_keys=[src_card_id])
    dst = relationship("Card", back_populates="received_transactions", foreign_keys=[dst_card_id])
