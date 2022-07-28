"""Клиент для выполнения методов Cloudpayments API"""

from asyncio import get_event_loop
from base64 import b64encode
from typing import Callable

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

    @property
    def __credentials(self) -> str:
        """Return decoded credentials (Public ID and API Secret)"""

        creds = f'{self.__public_id}:{self.__api_secret}'

        return b64encode(creds.encode()).decode("ascii")

    def __run_http_method(self, http_method: Callable, **kwargs) -> None:
        """Run HTTP method in event loop"""

        event_loop = get_event_loop()

        try:
            event_loop.run_until_complete(
                http_method(interaction_method='', **kwargs),
            )

            event_loop.run_until_complete(self.close())

            event_loop.close()
        except InteractionResponseError as error:
            print(error)

    def __send_request(self, url: str, http_method_name: str) -> None:
        """Send request to the URL with the HTTP method"""

        if http_method := self.__get_http_method(name=http_method_name):
            headers = {'Authorization': f'Basic {self.__credentials}'}

            self.__run_http_method(http_method, url=url, headers=headers)

    def __get_http_method(self, name: str) -> Callable | None:
        """Return HTTP method by name from AbstractInteractionClient"""

        http_methods = {
            # CRUD
            'post': self.post,
            'get': self.get,
            'put': self.put,
            'delete': self.delete,

            # Others
            'patch': self.patch,
        }

        return http_methods.get(name)


if __name__ == "__main__":
    cloudpayments_client = CloudpaymentsAPIClient("public_id", "api_secret")
    cloudpayments_client.charge()
