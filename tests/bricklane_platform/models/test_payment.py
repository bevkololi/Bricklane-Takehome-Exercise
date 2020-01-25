import unittest
from datetime import datetime

from bricklane_platform.models.payment import Payment
from bricklane_platform.models.card import Card
from bricklane_platform.models.bank import Bank


class TestPayment(unittest.TestCase):

    def test_init(self):
        payment = Payment()

        self.assertIsNone(payment.customer_id)
        self.assertIsNone(payment.date)
        self.assertIsNone(payment.amount)
        self.assertIsNone(payment.fee)
        self.assertIsNone(payment.card_id)
        self.assertIsNone(payment.bank_account_id)

    def test_init_with_data(self):

        data = {
            "amount": "2000",
            "card_id": "45",
            "card_status": "processed",
            "customer_id": "123",
            "date": "2019-02-01",
        }

        payment = Payment(data)

        self.assertEqual(payment.customer_id, 123)
        self.assertEqual(payment.date, datetime(2019, 2, 1))
        self.assertEqual(payment.amount, 1960)
        self.assertEqual(payment.fee, 40)


        card = payment.card

        self.assertIsInstance(card, Card)
        self.assertEqual(card.card_id, 45)
        self.assertEqual(card.status, "processed")

    def init_with_bank_data(self):

        bank_data = {
            "customer_id": "10",
            "date": "2020-01-10",
            "amount": "5000",
            "bank_account_id": "12"
        }

        bank_payment = Payment(bank_data)

        self.assertEqual(bank_payment.customer_id, 10)
        self.assertEqual(bank_payment.date, datetime(2020, 1, 10))
        self.assertEqual(bank_payment.amount, 4960)
        self.assertEqual(bank_payment.fee, 40)


    def test_is_successful(self):
        card = Card()
        card.status = "processed"
        payment = Payment()
        payment.card = card
        self.assertTrue(payment.is_successful())

    def test_bank_payment_is_successful(self):
        bank = Bank()
        bank.status = "processed"
        payment = Payment()
        payment.bank = bank
        self.assertTrue(payment.is_successful())

    def test_is_successful_declined(self):
        card = Card()
        card.status = "declined"
        payment = Payment()
        payment.card = card

        self.assertFalse(payment.is_successful())

    def test_is_successful_errored(self):
        card = Card()
        card.status = "errored"
        payment = Payment()
        payment.card = card

        self.assertFalse(payment.is_successful())
