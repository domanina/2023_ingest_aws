import pytest

from services.meta_srvcs.meta_api import Meta1API, Meta2API
from services.meta_srvcs.meta3_api import Meta3API


@pytest.fixture(scope="session")
def meta1_api_client():
    api = Meta1API()
    yield api


@pytest.fixture(scope="session")
def mata2_api_client():
    api = Meta2API()
    yield api


@pytest.fixture(scope="session")
def mata3_api_client():
    api = Meta3API()
    yield api
