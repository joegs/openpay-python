from datetime import datetime
from typing import Any, Dict

import openpay
from openpay.resource import ListableAPIResource, Card
from openpay import api, error
openpay.production = False
openpay.verify_ssl_certs = False

# openpay.api_key = OP_SECRET_KEY
# openpay.merchant_id = OP_OPENPAY_ID
openpay.country = 'mx'  #



class OpenPayUtils:

    def __init__(self, api_key, merchant_id):
        self.api_key = api_key
        self.merchant_id = merchant_id

    def get_all_customer(self):
        all_customer = openpay.Customer.all(api_key=self.api_key, merchant_id=self.merchant_id)
        return all_customer


    def create_customer(
        self, name: str, last_name: str, email: str, phone_number: str, external_id: str
    ):
        try:
            customer = openpay.Customer.create(
                name=name,
                email=email,
                last_name=last_name,
                phone_number=phone_number,
                external_id=external_id,
            )
            return customer.id

        except Exception as e:
            return {"error": e, "status": False}

    def retrieve_customer(self, id: str):

        customer = openpay.Customer.retrieve(id, api_key=self.api_key, merchant_id=self.merchant_id)
        return customer

        # except Exception as e:
        #     print("Error retrieve_customer", e)
        #     return None

    def retrive_customer_by_external_id(self, external_id: str):
        try:
            customer = openpay.Customer.all(external_id=external_id)
            return customer
        except Exception as e:
            print("Error retrieve_customer", e)
            return None

    def get_retrive_account(self, merchant_id: str, sk: str):
        # try:
        account = openpay.AccountInfo.all(api_key=sk, merchant_id=merchant_id)
        return account

        # except Exception as e:
        #     print('Error to get account', e)
        #     return {"error": e, "status": False}

    def add_card_to_customer(
        self, customer_id: str, card_id: str, device_session_id: str
    ):
        try:
            customer = self.retrieve_customer(customer_id)
            card = customer.cards.create(
                token_id=card_id, device_session_id=device_session_id
            )
            print("card created", card)
            return {"card": card, "status": True}

        except Exception as e:
            context = {"error": e, "status": False}
            return context

    def get_cards_of_customer(self, customer_id: str):
        # try:
            customer = self.retrieve_customer(customer_id)
            print("customer", customer)
            cards = customer.cards.all(api_key=self.api_key, merchant_id=self.merchant_id)
            return cards

        # except Exception as e:
        #     print("Error to get customer", e)
        #     return None

    def retrieve_card(self, customer_id: str, card_id: str):
        try:
            customer = self.retrieve_customer(customer_id)
            card = customer.cards.retrieve(card_id)
            return card

        except Exception as e:
            print("Error get card of customer", e)
            return None

    def delete_card_of_customer(self, customer_id: str, card_id=str):
        try:
            customer = self.retrieve_customer(customer_id)
            card = customer.cards.retrieve(card_id)
            card.delete()
            return {"status": "SUCCESS", "message": "Card deleted"}
        except Exception as e:
            print("Error delete card of customer", e)
            return {"status": "ERROR", "message": "Card not deleted"}

    def create_chargue(
        self,
        customer_id: str,
        card_id: str,
        amount: int,
        device_session_id: str,
        description,
        order_id,
        redirect_url=None,
    ):
        try:
            customer = self.retrieve_customer(customer_id)

            if amount < 5000:
                charge = customer.charges.create(
                    source_id=card_id,
                    amount=amount,
                    description=description,
                    device_session_id=device_session_id,
                    method="card",
                    currency="MXN",
                    order_id=order_id,
                    capture=True,
                )
            elif redirect_url:
                charge = customer.charges.create(
                    source_id=card_id,
                    amount=amount,
                    description=description,
                    device_session_id=device_session_id,
                    method="card",
                    currency="MXN",
                    order_id=order_id,
                    capture=True,
                    redirect_url=redirect_url,
                    use_3d_secure=True,
                )
            else:
                charge = None
        except Exception as e:
            context = {"error": str(e), "status": False}
            return context

        return {"charge": charge, "status": True}

    def update_card(
        self,
        customer_id: str,
        card_id: str,
        expiration_month: str = None,
        expiration_year: str = None,
        cvv2: str = None,
        holder_name: str = None,
    ):
        try:
            customer = self.retrieve_customer(customer_id)

            params = {
                "source_id": card_id,
                "expiration_month": expiration_month,
                "expiration_year": expiration_year,
                "cvv2": cvv2,
                "holder_name": holder_name,
            }

            card = customer.cards.save(**params)
            return card

        except Exception as e:
            print("Error get card of customer", e)
            return None

    def get_transaction_with_id(self, customer_id, transaction_id: str):
        print(customer_id, transaction_id)

        customer = self.retrieve_customer(customer_id)

        print("customer", customer)
        charge = customer.charges.retrieve(id=transaction_id)

        return charge
