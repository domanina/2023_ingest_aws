import json
import random
import string
import time
import uuid
import allure

from requests import Response
from consts.consts import Colors, TIMEOUT_SEC, RETRY
from tools.logger import get_logger

UNDEFINED_NAME = "undefined fun name"
logger = get_logger(name="main_logger")


def random_uuid() -> str:
    return str(uuid.uuid4())


@allure.step
def check_status_code(response: Response, status_code: int):
    assert response.status_code == status_code, \
        f"Test failed. HTTP status is : {response.status_code}, {response.text} (expected  HTTP status: {status_code})"


def pretty_log(response: Response, method: str, **kwargs):
    logger.info(f"{Colors.GREEN.value}{method} request to {response.url}{Colors.BLACK.value}")
    if kwargs.get("data") is not None:
        logger.info(f"{Colors.GREEN.value}Request body is {kwargs.get('data')}{Colors.BLACK.value}")
    logger.info(f"Response status is: {response.status_code}")
    logger.info(f"Response body is {response.text}")


def make_graphql_boby(query: str, variables: dict) -> str:
    return json.dumps({"query": query, "variables": variables})


def generate_random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def _wait(lambda_function, condition, delay, retry):
    condition_result = None
    function_result = None
    for _ in range(retry):
        try:
            function_result = lambda_function()
            logger.info(f"Actual result: [{function_result}], retry request...")
            condition_result = condition(function_result)
        except Exception as e:
            logger.error(f"Exception: {e}")
        if condition_result:
            return condition_result, function_result
        time.sleep(delay)
    return condition_result, function_result


def not_empty_wait(lambda_function, delay=TIMEOUT_SEC, retry=RETRY, function_name=UNDEFINED_NAME):
    condition_result, function_result = _wait(lambda_function, lambda result: result, delay, retry)
    assert condition_result, f"Response is empty: {function_name}"
    return function_result


def equal_wait(lambda_function, expected_data, delay=TIMEOUT_SEC, retry=RETRY):
    condition_result, function_result = _wait(
        lambda_function, lambda result: expected_data == result, delay, retry
    )
    error_msg = f"Expected value: {expected_data} doesnt match actual: {function_result}"
    assert condition_result, error_msg
    return function_result
