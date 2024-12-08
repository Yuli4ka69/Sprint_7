import requests
import allure
import logging
from requests.exceptions import RequestException
from helpers import generate_random_string
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
    @allure.step("Регистрация нового курьера")
    def register_new_courier(courier_data=None):
        """
        Регистрирует нового курьера и возвращает его данные (логин, пароль, имя, ID).
        Если данные о курьере не переданы, генерируются случайные данные.
        """
        if courier_data is None:
            courier_data = {
                "login": generate_random_string(),
                "password": generate_random_string(),
                "firstName": generate_random_string(),
            }

        # Отправляем запрос на создание курьера
        response = requests.post(CREATE_COURIER_URL, json=courier_data, timeout=30)

        # Если ответ 409, значит курьер с такими данными уже существует, и это нормально
        if response.status_code == 409:
            return {
                "login": courier_data["login"],
                "password": courier_data["password"],
                "firstName": courier_data["firstName"],
                "status_code": response.status_code
            }

        # Для других ошибок генерируем исключение
        if response.status_code != 201:
            raise requests.exceptions.HTTPError(
                f"{response.status_code} Client Error: {response.reason} for url: {response.url}"
            )

        # Авторизуемся, чтобы получить ID
        login_payload = {
            "login": courier_data["login"],
            "password": courier_data["password"],
        }
        auth_response = requests.post(COURIER_LOGIN_URL, json=login_payload, timeout=30)
        auth_response.raise_for_status()

        courier_id = auth_response.json().get("id")
        assert courier_id is not None, "Courier ID should not be None"

        return {
            "login": courier_data["login"],
            "password": courier_data["password"],
            "firstName": courier_data["firstName"],
            "id": courier_id,
            "status_code": response.status_code
        }

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
        url = DELETE_COURIER_URL.format(id=courier_id)
        response = requests.delete(url)
        response.raise_for_status()
        return response

    @staticmethod
    @allure.step("Проверка доступности сервера")
    def ping_server():
        logger.info(f"Request URL: {PING_SERVER_URL}")
        response = requests.get(PING_SERVER_URL, timeout=5)
        return CourierPage._handle_response(response)
