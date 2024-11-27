import requests
from urls import COURIER_URL, BASE_URL

class CourierPage:
    BASE_URL = COURIER_URL  # Используем URL из urls.py

    @staticmethod
    def create_courier(payload, client=requests):
        """Создать курьера через API."""
        return client.post(CourierPage.BASE_URL, json=payload)

    @staticmethod
    def delete_courier(courier_id):
        """Метод для удаления курьера по ID."""
        url = f"{BASE_URL}/{courier_id}"
        response = requests.delete(url)
        return response

    @staticmethod
    def login_courier(payload, client=requests):
        """Вход курьера через API."""
        return client.post(f"{CourierPage.BASE_URL}/login", json=payload)
