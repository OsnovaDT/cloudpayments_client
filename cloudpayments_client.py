"""Cloudpayments API client"""

from asyncio import get_event_loop
from base64 import b64encode

from aiohttp import TCPConnector

from abstract_client import AbstractInteractionClient, InteractionResponseError
from schemas import ChargePaymentSchema


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

        payment_data = ChargePaymentSchema().dump(payment)

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

    def __send_request(self, endpoint: str, headers: dict, json_=None) -> None:
        """Send request to the URL"""

        try:
            self.__event_loop.run_until_complete(self.post(
                interaction_method='', url=endpoint,
                headers=headers, json=json_,
            ))
        except InteractionResponseError as error:
            print(error)

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
