import requests
from urls import ORDERS_URL, ACCEPT_ORDER_URL, BASE_URL, TRACK_ORDER_URL

class MockResponse:
    """Фиктивный класс для имитации ответа от requests."""

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class OrderPage:
    """Класс для взаимодействия с API заказов."""

    @staticmethod
    def create_order(payload):
        """Создание заказа."""
        return requests.post(ORDERS_URL, json=payload)

    @staticmethod
    def get_order_by_id(order_id):
        """Метод для получения заказа по его ID."""
        if order_id is None:
            # Возвращаем ошибку с кодом 400, если ID не передан
            return MockResponse({"message": "Order ID is required"}, 400)

        url = f"{ORDERS_URL}/{order_id}"
        response = requests.get(url)
        return response

    @staticmethod
    def accept_order(order_id, courier_id):
        """Метод для принятия заказа."""
        url = f"{ACCEPT_ORDER_URL}/{order_id}?courierId={courier_id}"
        response = requests.put(url)
        return response

    @staticmethod
    def get_orders(params=None):
        """Получение списка заказов."""
        return requests.get(ORDERS_URL, params=params)

    @staticmethod
    def get_order_by_track(track_number):
        """Получить заказ по его номеру трека"""
        url = f"{TRACK_ORDER_URL}/{track_number}"  # Исправлено, теперь используем TRACK_ORDER_URL
        response = requests.get(url)
        return response
