from service.crud import Db
from service.database import Card


class TransactionPerformService:
    CROSS_BANK_COMISSION = 5 / 100
    SERVICE_COMISSION = 2 / 100
    NO_COMISSION_AMOUNT = 1000

    def __init__(self, src: Card, dst: Card, amount: float, db: Db):
        self.src = src
        self.dst = dst
        self.amount = amount
        self.db = db

    def perform(self):
        self.amount -= self.comission

    @property
    def comission(self):
        if self.amount >= self.NO_COMISSION_AMOUNT:
            return 0
        if self.dst.bank_name == self.src.bank_name:
            return self.amount * self.SERVICE_COMISSION

        return self.amount * (self.SERVICE_COMISSION + self.CROSS_BANK_COMISSION)
