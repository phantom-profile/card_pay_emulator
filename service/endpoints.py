from typing import Annotated

from fastapi import FastAPI, status, Depends, HTTPException

from service.models import (
    SignUpForm, SignUpResponse,
    MainInfo, TokenParam,
    CardForm, CardsList, CardRepresentation, TrustCardResponse,
    TransactionForm, TransactionResult
)
from service.crud import Db
from service.transactions import TransactionPerformService

Token = Annotated[TokenParam, Depends()]
app = FastAPI()
db = Db()


def get_user(token: TokenParam):
    user = db.get_user_by_token(token.token)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not authorized')
    return user


def get_card(card_id, user=None):
    card = db.get_card_by_id(card_id, user=user)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Card not found. Make sure that card "{card_id}" in your trusted cards list'
        )
    return card


@app.get("/")
def root() -> MainInfo:
    return MainInfo()


@app.post("/sign_up")
def register(data: SignUpForm) -> SignUpResponse:
    return db.create_user(data)


@app.post("/cards/trust")
def trust_card(card: CardForm, token: Token) -> TrustCardResponse:
    user = get_user(token)
    card = db.create_card(data=card, creator=user)
    return card


@app.get("/cards")
def get_cards(token: Token) -> CardsList:
    user = get_user(token)
    return CardsList(cards=[CardRepresentation.from_db(card) for card in user.cards])


@app.get("/transactions")
def get_transactions(token: Token) -> list[TransactionResult]:
    user = get_user(token)
    return CardsList(cards=[CardRepresentation.from_db(card) for card in user.cards])


@app.post("/cards/transaction")
def make_transaction(data: TransactionForm, token: Token) -> TransactionResult:
    user = get_user(token)
    src_card = get_card(data.src_card_uuid, user=user)
    dst_card = get_card(data.dst_card_uuid, user=user)
    result = TransactionPerformService(
        src=src_card, dst=dst_card, db=db, amount=data.money_amount_usd
    ).perform()

    return result
