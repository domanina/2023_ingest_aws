from typing import Optional

import requests

from requests import request, Response
from consts.consts import Colors
from tools.helper import pretty_log
from tools.logger import get_logger

logger = get_logger(name="main_logger")


class ApiClient:
    def __init__(self, url: str):
        assert url, "Url must be set"
        self._url = url

    @property
    def get_url(self):
        return self._url

    def _request(self, method: str, path: Optional[str], headers: Optional[dict], **kwargs) -> Response:

        url = self.get_url + path if path is not None else self.get_url

        try:
            response = request(method=method, url=url, headers=headers, verify=False, **kwargs)
            pretty_log(response=response, method=method, **kwargs)
            return response
        except requests.RequestException as e:
            logger.error(f"\n{Colors.RED.value}Request to '{path}' failed: {e}{Colors.BLACK.value}")

    def _get(self, path: Optional[str], **kwargs):
        return self._request("GET", path, **kwargs)

    def _delete(self, path: Optional[str], **kwargs):
        return self._request("DELETE", path, **kwargs)

    def _post(self, path: Optional[str], headers: dict, **kwargs):
        return self._request("POST", path, headers, **kwargs)

    def _put(self, path: Optional[str], **kwargs):
        return self._request("PUT", path, **kwargs)
