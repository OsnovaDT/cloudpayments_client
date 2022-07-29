"""Cloudpayments API client"""

from asyncio import get_event_loop
from base64 import b64encode, b64decode

from aiohttp import TCPConnector
from marshmallow import ValidationError
from loguru import logger
from transaction import begin

from abstract_client import AbstractInteractionClient, InteractionResponseError
from schemas import ChargeTokenPaymentSchema


class CloudPaymentsAPIClient(AbstractInteractionClient):
    """Contains CloudPayments API methods.

    For initialization specify Public ID and API Secret.

    """

    def __init__(self, public_id: str, api_secret: str):
        super().__init__()

        self.__public_id = public_id
        self.__api_secret = api_secret

        self.__event_loop = get_event_loop()

        self.BASE_URL = 'https://api.cloudpayments.ru'
        self.CONNECTOR = TCPConnector()
        self.SERVICE = 'cloudpayments'

    def __del__(self):
        self.CONNECTOR.close()
        self.__event_loop.close()

    def charge(self, payment: dict) -> None:
        """API charge method - single-stage payment"""

        if payment_data := self.__get_payment_data(payment):
            charge_endpoint = self.endpoint_url('payments/cards/charge/')

            headers = self.__get_headers(is_auth=True)

            self.__send_request(charge_endpoint, headers, payment_data)

    def test(self, request_id=None) -> None:
        """API test method - check interaction with API"""

        test_endpoint = self.endpoint_url('test/')

        headers = self.__get_headers(request_id, True)

        self.__send_request(test_endpoint, headers)

    @property
    def __credentials(self) -> str:
        """Return decoded credentials (Public ID and API Secret)"""

        creds = f'{self.__public_id}:{self.__api_secret}'

        return b64encode(creds.encode()).decode("ascii")

    def __get_payment_data(self, payment) -> dict:
        """Return payment data in JSON format"""

        if 'Token' in payment.keys():
            payment['Token'] = str(b64decode(payment.get('Token')))

        try:
            payment_data = ChargeTokenPaymentSchema().load(payment)
        except ValidationError as error:
            payment_data = {}
            logger.error(error)

        return payment_data

    def __send_request(self, endpoint: str, headers: dict, json_=None) -> None:
        """Send request to the URL"""

        transaction_ = begin()

        try:
            self.__event_loop.run_until_complete(
                self.post(
                    interaction_method='', url=endpoint,
                    headers=headers, json=json_,
                ),
            )

            transaction_.commit()
        except InteractionResponseError as error:
            logger.error(error)

            transaction_.abort()

        self.__event_loop.run_until_complete(self.close())

    def __get_headers(self, request_id=None, is_auth=False) -> dict:
        """Return headers for HTTP request"""

        headers = {}

        if is_auth:
            headers['Authorization'] = f'Basic {self.__credentials}'

        if request_id:
            # Make the request idempotent
            headers['X-Request-ID'] = request_id

        return headers
