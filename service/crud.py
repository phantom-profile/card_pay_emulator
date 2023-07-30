from sqlite3 import DatabaseError

from uuid import uuid4, UUID

from sqlalchemy.exc import SQLAlchemyError

from service.database import Card, User, Transaction, SessionLocal
from service.models import SignUpForm, SignUpResponse, CardForm, TrustCardResponse, TransactionResult


import functools


def rollback_on_fail(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (DatabaseError, SQLAlchemyError) as error:
            self = args[0]
            self.session.rollback()
            raise error
    return func


class Db:
    def __init__(self):
        self.session = SessionLocal()

    def get_user_by_token(self, token: UUID) -> User | None:
        user = self.session.query(User).filter(User.token == token).first()
        return user

    def get_card_by_id(self, card_id: UUID, user: User = None) -> Card | None:
        cards_scope = self.session.query(Card).filter(Card.id == card_id)
        if user:
            cards_scope = cards_scope.filter(Card.trusted_app_id == user.id)
        return cards_scope.first()

    def get_transactions(self, user: User) -> list[Transaction]:
        return user.transactions_query().with_session(self.session).all()

    @rollback_on_fail
    def create_user(self, data: SignUpForm):
        user = User(
            app_name=data.app_name,
            token=uuid4()
        )
        self.session.add(user)
        self.session.commit()
        return SignUpResponse(access_token=user.token, app_name=user.app_name)

    @rollback_on_fail
    def create_card(self, data: CardForm, creator: User) -> TrustCardResponse:
        card = Card(
            card_number=data.card_number,
            cvv=data.cvv,
            bank_name=data.bank_name,
            owner=data.owner,
            payment_system=data.payment_system,
            trusted_app_id=creator.id
        )
        self.session.add(card)
        self.session.commit()
        self.session.refresh(card)

        return TrustCardResponse(
            card_number=card.card_number,
            card_uuid=card.id,
            card_user=creator.app_name
        )

    @rollback_on_fail
    def create_transaction(self, data: TransactionResult) -> Transaction:
        transaction = Transaction(
            src_card_id=data.src_card_uuid,
            dst_card_id=data.dst_card_uuid,
            status=data.status.value,
            amount_usd=data.money_amount_usd
        )
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)

        return transaction

    def __del__(self):
        print('closing session')
        self.session.close()
