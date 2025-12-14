import datetime


class Card:
    def __init__(self, card_holder, card_number, expiration_date, cvv):
        if self._validate_card_holder(card_holder):
            self.card_holder = card_holder
        if self._validate_card_number(card_number):
            self._card_number = card_number
        if self._validate_expiration_date(expiration_date):
            self._expiration_date = expiration_date
        if self._validate_cvv(cvv):
            self._cvv = cvv

    @staticmethod
    def _validate_card_holder(card_holder):
        if isinstance(card_holder, str):
            return True
        else:
            raise TypeError("Must be a string.")

    @staticmethod
    def _validate_card_number(card_number):
        if isinstance(card_number, int):
            if 15 <= card_number <= 16:
                return True
            else:
                raise ValueError("Card number must have 15 or 16 numeric characters.")
        else:
            raise TypeError("Digits only.")

    @staticmethod
    def _validate_expiration_date(expiration_date):
        today = datetime.date.today()
        if expiration_date > today:
            return True
        else:
            raise ValueError("Card expired.")

    @staticmethod
    def _validate_cvv(cvv):
        if isinstance(cvv, int):
            if 3 <= len(cvv) <= 4:
                return True
            else:
                raise ValueError("Invalid CVV length.")
        else:
            raise TypeError("Digits only.")

