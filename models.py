from enum import StrEnum
from typing import ClassVar
from uuid import uuid4, UUID

from dotenv import dotenv_values
from pydantic import BaseModel, Field, field_validator, confloat

env_variables = dotenv_values(".env")

UsdAmount = confloat(gt=0, lt=1_000_000)


class TransactionStatuses(StrEnum):
    SUCCESS = 'SUCCESS'
    REJECTED = 'REJECTED'
    FAILED = 'FAILED'


class MainInfo(BaseModel):
    created_by: str = env_variables['AUTHOR']
    doc_url: str = env_variables['DOCS_URL']
    description: str = env_variables['DESCRIPTION']


class SignUpForm(BaseModel):
    app_name: str = Field(max_length=50, pattern=r'^[a-zA-Z_]{3,50}$', examples=['my_app'])


class SignUpResponse(SignUpForm):
    access_token: UUID = Field(examples=[uuid4()])


class TokenParam(BaseModel):
    token: UUID = Field(examples=[uuid4()])


class CardForm(BaseModel):
    SYSTEMS: ClassVar = ['VISA', 'MIR', 'MASTER CARD', 'MAESTRO']

    card_number: str = Field(pattern=r'[0-9]{16}', min_length=16, max_length=16)
    cvv: str = Field(pattern=r'[0-9]{3}', min_length=3, max_length=3)
    owner: str = Field(pattern=r'^[A-Z ]{3,50}$')
    payment_system: str = Field(examples=SYSTEMS)

    @field_validator('payment_system')
    @classmethod
    def known_payment_system(cls, value: str) -> str:
        if value not in cls.SYSTEMS:
            raise ValueError(f'Unknown payment system. Possible variants: {cls.SYSTEMS}')
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "card_number": "1234123412341234",
                    "cvv": "000",
                    "owner": "FIRSTNAME LASTNAME",
                    "payment_system": SYSTEMS[0],
                }
            ]
        }
    }


class TrustCardResponse(BaseModel):
    card_number: str = Field(examples=["1234123412341234"])
    card_uuid: UUID = Field(examples=[uuid4()])
    card_user: str = Field(examples=['my_app'])


class CardRepresentation(CardForm):
    card_uuid: UUID = Field(examples=[uuid4()])
    card_user: str = Field(examples=['my_app'])


class CardsList(BaseModel):
    cards: list[CardRepresentation]


class TransactionForm(BaseModel):
    src_card_uuid: UUID = Field(examples=[uuid4()])
    dst_card_uuid: UUID = Field(examples=[uuid4()])
    money_amount_usd: UsdAmount


class TransactionResult(TransactionForm):
    status: TransactionStatuses
