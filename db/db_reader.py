import allure

from config.config import USERNAME, PASSWORD
from db.msql_client import MySQLClient
from tools.singleton import Singleton


class DBReader(MySQLClient, metaclass=Singleton):
    def __init__(self):
        super().__init__(
            server_name=HOST,
            db_name=DATABASE_NAME,
            password=PASSWORD,
            username=USERNAME
        )

    @allure.step("Select ...")
    def select_order_group(self, item_id: str):
        result = self.execute(SELECT_ITEM, (item_id,))
        return result