from typing import Annotated

from fastapi import FastAPI, status, Depends, HTTPException

from models import SignUpResponse, SignUpForm, MainInfo, CardForm, TrustCardResponse, TransactionForm, TransactionResult, TokenParam, TransactionStatuses, CardsList, CardRepresentation
from crud import Db

Token = Annotated[TokenParam, Depends()]
app = FastAPI()
db = Db()


def get_user(token: TokenParam):
    user = db.get_user_by_token(token.token)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not authorized')
    return user


@app.get("/")
def root() -> MainInfo:
    return MainInfo()


@app.post("/sign_up")
def register(data: SignUpForm) -> SignUpResponse:
    return db.create_user(data)


@app.post("/cards/trust", response_model=TrustCardResponse)
def trust_card(card: CardForm, token: Token):
    user = get_user(token)
    card = db.create_card(data=card, creator=user)
    return card


@app.get("/cards", response_model=CardsList)
def get_cards(token: Token):
    user = get_user(token)
    cards = []
    for card in user.cards:
        card_repr = CardRepresentation(
            card_number=card.card_number,
            cvv=card.cvv,
            owner=card.owner,
            payment_system=card.payment_system,
            card_uuid=card.id,
            card_user=user.app_name
        )
        cards.append(card_repr)
    return CardsList(cards=cards)


@app.post("/cards/transaction", response_model=TransactionResult)
def make_transaction(data: TransactionForm, token: Token):
    user = get_user(token)
    src_card = db.get_card_by_id(data.src_card_uuid, user=user)
    dst_card = db.get_card_by_id(data.dst_card_uuid, user=user)
    if not src_card or not dst_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Cards not found. Make sure that this cards in your trusted cards list'
        )

    return TransactionResult(
        dst_card_uuid=src_card.id,
        src_card_uuid=dst_card.id,
        status=TransactionStatuses.SUCCESS,
        money_amount_usd=data.money_amount_usd
    )
