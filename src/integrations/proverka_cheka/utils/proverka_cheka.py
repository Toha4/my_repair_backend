import json
from typing import TypedDict

import requests


class ReceiptsItems(TypedDict):
    name: str
    price: float
    quantity: int


class Receipts(TypedDict):
    shop_name: str
    date_time: str
    items: list[ReceiptsItems]


class ProverkaCheka:
    """Класс для получение информации по чекам https://proverkacheka.com"""

    def __init__(self, token: str) -> None:
        self.__url = "https://proverkacheka.com/api/v1/check/get"
        self.__token = token

    def get_check_qrraw(self, qrraw: str) -> Receipts:
        """Получить информации по чеку использую текст с qr-кода"""

        response = requests.post(self.__url, data={"token": self.__token, "qrraw": qrraw})
        data = json.loads(response.content)["data"]["json"]

        receipts: Receipts = {
            "shop_name": data["user"],
            "date_time": data["dateTime"],
            "items": [self.__parce_item(item) for item in data["items"]],
        }

        return receipts

    def __parce_item(self, receipt_item) -> ReceiptsItems:
        item: ReceiptsItems = {
            "name": receipt_item["name"],
            "price": receipt_item["price"] / 100,
            "quantity": receipt_item["quantity"],
        }

        return item
