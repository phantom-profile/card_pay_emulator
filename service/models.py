from datetime import datetime
from enum import Enum
from random import choice
from typing import ClassVar
from uuid import uuid4, UUID

from dotenv import dotenv_values
from pydantic import BaseModel, Field, field_validator, confloat, model_validator

from service.database import Card, Transaction

env_variables = dotenv_values(".env")

UsdAmount = confloat(gt=0, lt=1_000_000)


class TransactionStatuses(Enum):
    SUCCESS = 'SUCCESS'
    REJECTED = 'REJECTED'
    FAILED = 'FAILED'

    @classmethod
    def random(cls):
        return choice([cls.SUCCESS, cls.SUCCESS, cls.FAILED, cls.REJECTED])


class MainInfo(BaseModel):
    created_by: str = env_variables['AUTHOR']
    doc_url: str = env_variables['DOCS_URL']
    description: str = env_variables['DESCRIPTION']


class SignUpForm(BaseModel):
    app_name: str = Field(max_length=50, pattern=r'^[a-zA-Z0-9_]{3,50}$', examples=['my_app'])


class SignUpResponse(SignUpForm):
    access_token: UUID = Field(examples=[uuid4()])


class TokenParam(BaseModel):
    token: UUID = Field(examples=[uuid4()])


class CardForm(BaseModel):
    SYSTEMS: ClassVar = ['VISA', 'MIR', 'MASTER CARD', 'MAESTRO']
    BANKS: ClassVar = ['Sber', 'Tinkoff', 'Kaspi', 'VTB', 'Gazprom', 'Unicredit']

    card_number: str = Field(
        pattern=r'[0-9]{16}',
        min_length=16, max_length=16,
        examples=['1234123412341234']
    )
    cvv: str = Field(pattern=r'[0-9]{3}', min_length=3, max_length=3, examples=['000'])
    owner: str = Field(pattern=r'^[A-Z ]{3,50}$', examples=["FIRSTNAME LASTNAME"])
    payment_system: str = Field(examples=SYSTEMS)
    bank_name: str = Field(examples=BANKS)

    @field_validator('payment_system')
    @classmethod
    def known_payment_system(cls, value: str) -> str:
        if value not in cls.SYSTEMS:
            raise ValueError(f'Unknown payment system. Possible variants: {cls.SYSTEMS}')
        return value

    @field_validator('bank_name')
    @classmethod
    def validate_bank_name(cls, value: str) -> str:
        if value not in cls.BANKS:
            raise ValueError(f'Unknown bank. Possible variants: {cls.BANKS}')
        return value


class TrustCardResponse(BaseModel):
    card_number: str = Field(examples=["1234123412341234"])
    card_uuid: UUID = Field(examples=[uuid4()])
    card_user: str = Field(examples=['my_app'])


class CardRepresentation(CardForm):
    card_uuid: UUID = Field(examples=[uuid4()])
    card_user: str = Field(examples=['my_app'])

    @classmethod
    def from_db(cls, card: Card):
        return cls(
            card_number=card.card_number,
            cvv=card.cvv,
            owner=card.owner,
            payment_system=card.payment_system,
            card_uuid=card.id,
            bank_name=card.bank_name,
            card_user=card.trusted_app.app_name
        )


class CardsList(BaseModel):
    cards: list[CardRepresentation]


class TransactionForm(BaseModel):
    src_card_uuid: UUID = Field(examples=[uuid4()])
    dst_card_uuid: UUID = Field(examples=[uuid4()])
    money_amount_usd: UsdAmount

    @model_validator(mode='after')
    def validate_dst_card_uuid(self):
        if self.src_card_uuid == self.dst_card_uuid:
            raise ValueError('Source and destination cards must be different')
        return self


class TransactionResult(TransactionForm):
    status: TransactionStatuses
    comission: confloat(ge=0, lt=1_000_000)
    created_at: datetime

    @classmethod
    def from_db(cls, transaction: Transaction):
        return cls(
            src_card_uuid=transaction.src_card_id,
            dst_card_uuid=transaction.dst_card_id,
            money_amount_usd=transaction.amount_usd,
            status=transaction.status,
            comission=transaction.comission,
            created_at=transaction.created_at
        )


class TransactionsFilter(BaseModel):
    amount_gt: int
    status_eq: TransactionStatuses
    src_card_uuid_eq: UUID = Field(examples=[uuid4()])
    dst_card_uuid_eq: UUID = Field(examples=[uuid4()])


class TransactionsList(BaseModel):
    transactions: list[TransactionResult]
