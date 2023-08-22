
from openpaymodule import OpenPayUtils
# import openpay



# create main

if __name__ == "__main__":
    sk = "sk_9a3241ac946943558f38f6a10e312ea7"
    merchant_id = "mrbgtcbxwcchv4m1de1t"
    
    openpay_utils = OpenPayUtils(
        api_key=sk, merchant_id=merchant_id
    )

    # response = openpay_utils.get_all_customer()

    response = openpay_utils.get_cards_of_customer(customer_id="adzelgcsofmff8afiacx")

    print(response)