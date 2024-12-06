import allure
import requests
import logging
from requests.exceptions import RequestException
from urls import ORDERS_URL, ACCEPT_ORDER_URL, TRACK_ORDER_URL


logger = logging.getLogger(__name__)

class OrderPage:
    """Класс для взаимодействия с API заказов."""

    @staticmethod
    def _validate_required_param(param, param_name):
        if not param:
            raise ValueError(f"{param_name} is required")

    @staticmethod
    def _handle_response(response):
        try:
            response.raise_for_status()
        except RequestException as e:
            logger.error(f"Request failed: {e}, Response: {response.text}")
            allure.attach(response.text, name="Error Response", attachment_type=allure.attachment_type.TEXT)
            raise
        return response

    @staticmethod
    @allure.step("Создание заказа с данными: {payload}")
    def create_order(payload):
        response = requests.post(ORDERS_URL, json=payload)
        response.raise_for_status()
        return response

    @staticmethod
    @allure.step("Получение заказа по трек-номеру: {track_number}")
    def get_order_by_track(track_number):
        OrderPage._validate_required_param(track_number, "Track number")
        response = requests.get(f"{TRACK_ORDER_URL}?t={track_number}")
        return response

    @staticmethod
    @allure.step("Принятие заказа с ID: {order_id} курьером с ID: {courier_id}")
    def accept_order(order_id, courier_id):
        OrderPage._validate_required_param(order_id, "Order ID")
        OrderPage._validate_required_param(courier_id, "Courier ID")
        url = f"{ACCEPT_ORDER_URL}/{order_id}?courierId={courier_id}"
        response = requests.put(url)
        return OrderPage._handle_response(response)
