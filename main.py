"""For running CloudPaymentsAPIClient"""

from base64 import b64encode

from cloudpayments_client import CloudPaymentsAPIClient


if __name__ == "__main__":
    cloudpayments_client = CloudPaymentsAPIClient("public_id", "api_secret")

    print('### Method test ###')
    cloudpayments_client.test()

    print('\n### Method charge ###')
    cloudpayments_client.charge({
        "Amount": 59,
        "Currency": "RUB",
        "InvoiceId": "1234567",
        "Description": "Оплата товаров в example.com",
        "AccountId": "user_x",
        "Token": b64encode(b"success_1111a3e0-2428-48fb-a530-12815d90"),
        "Payer": {
            "FirstName": "Тест",
            "LastName": "Тестов",
            "MiddleName": "Тестович",
            "Address": "тестовый проезд дом тест",
            "Street": "Lenina",
            "City": "MO",
            "Country": "RU",
            "Phone": 123,
            "Postcode": 345,
        },
    })
