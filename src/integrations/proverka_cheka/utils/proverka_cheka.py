import datetime
import json
from typing import TypedDict

import requests


class ReceiptItemType(TypedDict):
    name: str
    price: float
    quantity: float
    sum: float


class ReceiptType(TypedDict):
    qr_raw: str
    organization: str
    retail_place_addres: str
    organization_inn: str
    date: datetime.datetime
    request_number: int
    operator: str
    total_sum: float
    html: str
    items: list[ReceiptItemType]


class ProverkaCheka:
    """Класс для получение информации по чекам https://proverkacheka.com"""

    def __init__(self, token: str) -> None:
        self.__url = "https://proverkacheka.com/api/v1/check/get"
        self.__token = token

    def get_check_qrraw(self, qrraw: str) -> ReceiptType:
        """Получить информации по чеку использую текст с qr-кода"""

        response = requests.post(self.__url, data={"token": self.__token, "qrraw": qrraw})
        response_content = json.loads(response.content)
        data = response_content["data"]["json"]

        receipts: ReceiptType = {
            "qr_raw": qrraw,
            "organization": data.get("user", ""),
            "retail_place_addres": data.get("retailPlace", ""),
            "organization_inn": data.get("userInn", ""),
            "date": datetime.datetime.strptime(data.get("dateTime"), "%Y-%m-%dT%H:%M:%S"),
            "request_number": int(data.get("requestNumber")) if data.get("requestNumber") else None,
            "operator": data.get("operator", ""),
            "total_sum": data["totalSum"] / 100,
            "html": response_content["data"]["html"],
            "items": [self.__parce_item(item) for item in data["items"]],
        }

        return receipts

    def __parce_item(self, receipt_item) -> ReceiptItemType:
        item: ReceiptItemType = {
            "name": receipt_item["name"],
            "price": receipt_item["price"] / 100,
            "quantity": receipt_item["quantity"],
            "sum": receipt_item["sum"] / 100,
        }

        return item
