from service.database import Card
from service.models import TransactionResult, TransactionStatuses


class TransactionPerformService:
    CROSS_BANK_COMISSION = 5 / 100
    SERVICE_COMISSION = 2 / 100
    NO_COMISSION_AMOUNT = 1000

    def __init__(self, src: Card, dst: Card, amount: float, db):
        self.src = src
        self.dst = dst
        self.amount = amount
        self.db = db
        self.status = None

    def perform(self):
        self.status = self.request_transaction()
        result = TransactionResult(
            src_card_uuid=self.src.id,
            dst_card_uuid=self.dst.id,
            money_amount_usd=self.amount - self.comission,
            status=self.status,
            comission=self.comission
        )
        self.db.create_transaction(result)
        return result

    @property
    def comission(self):
        if self.status != TransactionStatuses.SUCCESS:
            return 0

        comission_percent = 0
        if self.dst.bank_name != self.src.bank_name:
            comission_percent += self.CROSS_BANK_COMISSION
        if self.amount < self.NO_COMISSION_AMOUNT:
            comission_percent += self.SERVICE_COMISSION

        return self.amount * comission_percent

    def request_transaction(self):
        # emulating API call to bank system
        return TransactionStatuses.random()
