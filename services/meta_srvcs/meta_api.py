import allure

from requests import Response
from services.api_client.api_client import ApiClient
from tools.singleton import Singleton


class Meta1API(ApiClient, metaclass=Singleton):
    def __init__(self, url=URL):
        super().__init__(url=url)

    @allure.step("...")
    def post_meta1_data(self, payload: str, headers: dict) -> Response:
        return self._post(path=None, data=payload, headers=headers)


class Meta2API(ApiClient, metaclass=Singleton):
    def __init__(self, url=URL):
        super().__init__(url=url)

    @allure.step("...")
    def post_meta2_data(self, payload: str, headers: dict) -> Response:
        return self._post(path=None, data=payload, headers=headers)
