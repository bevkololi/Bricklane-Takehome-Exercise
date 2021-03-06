from decimal import Decimal
from dateutil.parser import parse


from bricklane_platform.models.card import Card
from bricklane_platform.models.bank import Bank
from bricklane_platform.config import PAYMENT_FEE_RATE


class Payment(object):

    customer_id = None
    bank_account_id = None
    date = None
    amount = None
    fee = None
    card_id = None

    def __init__(self, data=None):

        if not data:
            return

        self.customer_id = int(data["customer_id"])
        self.date = parse(data["date"])

        total_amount = Decimal(data["amount"])
        self.fee = total_amount * PAYMENT_FEE_RATE
        self.amount = total_amount - self.fee

        try:
            card_id = data["card_id"]
            card = Card()
            card.card_id = int(card_id)
            card.status = data["card_status"]
            self.card = card
        except:
            bank_account_id = data["bank_account_id"]
            bank = Bank()
            bank.bank_account_id = int(bank_account_id)
            self.bank = bank


    def is_successful(self):
        try:
            return self.card.status == "processed"
        except AttributeError as error:
            return error
        else:
            return self.bank.status == "processed"