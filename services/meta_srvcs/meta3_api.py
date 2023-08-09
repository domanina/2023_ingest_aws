import allure

from requests import Response
from services.api_client.api_client import ApiClient
from tools.singleton import Singleton


class Meta3API(ApiClient, metaclass=Singleton):
    def __init__(self, url=URL):
        super().__init__(url=url)

    @allure.step("...")
    def get_meta3_data(self, params: dict) -> Response:
        return self._get(path=None, headers=None, params=params)
