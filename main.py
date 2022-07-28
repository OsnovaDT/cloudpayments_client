"""For running CloudPaymentsAPIClient"""

from datetime import date

from cloudpayments_client import CloudPaymentsAPIClient


if __name__ == "__main__":
    cloudpayments_client = CloudPaymentsAPIClient("public_id", "api_secret")

    print('### Method test ###')
    cloudpayments_client.test()

    print('\n### Method charge ###')
    cloudpayments_client.charge({
        "Amount": 10,
        "Currency": "RUB",
        "InvoiceId": 1234567,
        "IpAddress": "123.123.123.123",
        "Description": "Оплата товаров в example.com",
        "AccountId": "user_x",
        "Name": "CARDHOLDER NAME",
        "CardCryptogramPacket": "01492500008719030128SMf",
        "Payer": {
            "FirstName": "Тест",
            "LastName": "Тестов",
            "MiddleName": "Тестович",
            "Birth": date(1955, 2, 24),
            "Address": "тестовый проезд дом тест",
            "Street": "Lenina",
            "City": "MO",
            "Country": "RU",
            "Phone": 123,
            "Postcode": 345,
        },
    })
