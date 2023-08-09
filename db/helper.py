from datetime import datetime
from typing import Optional

import allure

from consts.consts import Colors
from db.db_reader import DBReader
from tools.helper import not_empty_wait
from tools.logger import get_logger

logger = get_logger(name="main_logger")
db_reader = DBReader()


def get_db_data(query: str, params: Optional[tuple] = None, wait_until: Optional[bool] = False) -> tuple:
    if not wait_until:
        res = db_reader.execute(query=query, params=params)
    else:
        res = wait_until(query=query, params=params)
    return res


def verify_db_data(query: str, params: Optional[tuple] = None):
    res = db_reader.execute(query, params)
    assert res is not None
    assert res[0] == "SUCCESS", logger.debug(
        f"{Colors.YELLOW.value}Task status in DB still is not in SUCCESS [{res}], retry request...{Colors.BLACK.value}")
    return res


def wait_until(query: str, params: Optional[tuple] = None):
    with allure.step("Try to get data"):
        start_time = datetime.now()
        response = not_empty_wait(
                lambda:
                verify_db_data(query, params), function_name="verify_sql_data")
        dif_time = (datetime.now() - start_time).seconds
        logger.debug(f"--------->Time spent on execution: {dif_time} seconds")
    return response
