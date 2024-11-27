import requests
from urls import COURIER_LOGIN_URL

class CourierLoginPage:
    BASE_URL = COURIER_LOGIN_URL

    @staticmethod
    def login(payload):
        """Отправляет запрос на авторизацию курьера."""
        return requests.post(CourierLoginPage.BASE_URL, json=payload)
