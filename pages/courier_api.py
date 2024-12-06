import requests
import allure
import logging
from requests.exceptions import RequestException
from urls import (
    COURIER_LOGIN_URL,
    CREATE_COURIER_URL,
    DELETE_COURIER_URL,
    PING_SERVER_URL,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CourierPage:
    """API для работы с курьерами."""

    @staticmethod
    def _handle_response(response):
        """Унифицированная обработка ответов API."""
        try:
            response.raise_for_status()
        except RequestException as e:
            logger.error(f"Request failed: {e}, Response: {response.text}")
            allure.attach(response.text, name="Error Response", attachment_type=allure.attachment_type.TEXT)
            raise
        return response

    @staticmethod
    @allure.step("Создание курьера")
    def create_courier(payload):
        """
        Создание курьера.
        """
        try:
            response = requests.post(CREATE_COURIER_URL, json=payload, timeout=30)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            allure.attach(str(response.text), name="HTTP Error Response", attachment_type=allure.attachment_type.TEXT)
            return response  # Возвращаем ответ, чтобы тест его обработал
        return response

    @staticmethod
    @allure.step("Авторизация курьера с данными: {payload}")
    def login_courier(payload):
        """
        Метод для авторизации курьера.

        :param payload: Данные для авторизации
        :return: Ответ API
        """
        response = requests.post(COURIER_LOGIN_URL, json=payload)
        return response

    @staticmethod
    @allure.step("Удаление курьера с ID: {courier_id}")
    def delete_courier(courier_id):
        """
        Удаление курьера по ID.

        :param courier_id: ID курьера
        :return: Ответ API
        """
        url = DELETE_COURIER_URL.format(id=courier_id)  # Используем URL из data.py
        response = requests.delete(url)
        response.raise_for_status()  # Генерирует исключение при ошибке
        return response

    @staticmethod
    @allure.step("Проверка доступности сервера")
    def ping_server():
        logger.info(f"Request URL: {PING_SERVER_URL}")
        response = requests.get(PING_SERVER_URL, timeout=5)
        return CourierPage._handle_response(response)
