from sqlite3 import DatabaseError

from uuid import uuid4, UUID

from sqlalchemy.exc import SQLAlchemyError

from service.database import Card, User, Transaction, SessionLocal
from service.models import SignUpForm, SignUpResponse, CardForm, TrustCardResponse, TransactionForm


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
            owner=data.owner,
            payment_system=data.payment_system,
            trusted_app_id=creator.id,
        )
        self.session.add(card)
        self.session.commit()
        self.session.refresh(card)

        return TrustCardResponse(
            card_number=card.card_number,
            card_uuid=card.id,
            card_user=creator.app_name
        )

    def create_transaction(self, data: TransactionForm):
        pass

    def __del__(self):
        print('closing session')
        self.session.close()
