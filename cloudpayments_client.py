"""Клиент для выполнения методов Cloudpayments API"""

from asyncio import get_event_loop
from base64 import b64encode

from aiohttp import TCPConnector

from abstract_client import AbstractInteractionClient, InteractionResponseError


class CloudpaymentsAPIClient(AbstractInteractionClient):
    """Cloudpayments API client"""

    def __init__(self, public_id: str, api_secret: str):
        self.__public_id = public_id
        self.__api_secret = api_secret

        super().__init__()

        self.BASE_URL = 'https://api.cloudpayments.ru'
        self.CONNECTOR = TCPConnector()
        self.SERVICE = 'service'

    def charge(self) -> None:
        """Implement charge method - single-stage payment"""

        charge_endpoint = self.endpoint_url('payments/cards/charge/')

        self.__send_request(charge_endpoint, 'post')

    def test(self) -> None:
        """Implement test method - check interaction with API"""

        test_endpoint = self.endpoint_url('test/')

        self.__send_request(test_endpoint, 'post')

    @property
    def __credentials(self) -> str:
        """Return decoded credentials (Public ID and API Secret)"""

        creds = f'{self.__public_id}:{self.__api_secret}'

        return b64encode(creds.encode()).decode("ascii")

    def __send_post(self, **kwargs) -> None:
        """Run POST method in event loop"""

        event_loop = get_event_loop()

        try:
            event_loop.run_until_complete(
                self.post(interaction_method='', **kwargs),
            )
        except InteractionResponseError as error:
            print(error)

        event_loop.run_until_complete(self.close())
        self.CONNECTOR.close()
        event_loop.close()

    def __send_request(self, url: str, request_id=None) -> None:
        """Send request to the URL with the HTTP method"""

        headers = {
            'Authorization': f'Basic {self.__credentials}',
        }

        if request_id:
            headers['X-Request-ID'] = request_id

        self.__send_post(url=url, headers=headers)


if __name__ == "__main__":
    cloudpayments_client = CloudpaymentsAPIClient("public_id", "api_secret")
    # cloudpayments_client.charge()
    cloudpayments_client.test()
