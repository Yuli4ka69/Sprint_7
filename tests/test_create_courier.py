import allure
import requests
from pages.courier_api import CourierPage
from urls import CREATE_COURIER_URL
from data import (
    HTTP_STATUS_BAD_REQUEST,
    HTTP_STATUS_CONFLICT,
    ERROR_MESSAGE_DUPLICATE_LOGIN,
    ERROR_MESSAGE_MISSING_COURIER_FIELDS
)

@allure.feature("Courier API")
@allure.story("Create Courier")
class TestCreateCourier:
    """Тесты для создания курьера."""

    @allure.title("Test successful courier creation")
    def test_create_courier_success(self, create_courier):
        """Проверка успешного создания курьера."""
        courier_data = create_courier  # Получаем данные курьера
        assert courier_data['id'] is not None, "Courier ID should not be None after successful creation"
        assert courier_data['login'] is not None, "Courier login should not be None"
        assert courier_data['password'] is not None, "Courier password should not be None"
        assert courier_data['firstName'] is not None, "Courier firstName should not be None"

    def test_create_courier_duplicate(self, create_courier):
        """Нельзя создать двух одинаковых курьеров с одинаковыми данными."""
        courier_data = create_courier

        duplicate_courier_data = {
            "login": courier_data["login"],
            "password": courier_data["password"],
            "firstName": courier_data["firstName"]
        }

        response_duplicate = CourierPage.register_new_courier(duplicate_courier_data)

        assert response_duplicate["status_code"] == HTTP_STATUS_CONFLICT, (
            f"Expected status code {HTTP_STATUS_CONFLICT}, got {response_duplicate['status_code']}"
        )

    @allure.title("Test courier creation with missing fields")
    def test_create_courier_missing_fields(self):
        """Тест для проверки ошибки при создании курьера с отсутствующими обязательными полями."""

        # Отправляем запрос без логина
        payload_missing_login = {
            "password": "password123",
            "firstName": "New Courier"
        }
        response_missing_login = requests.post(CREATE_COURIER_URL, json=payload_missing_login)
        assert response_missing_login.status_code == HTTP_STATUS_BAD_REQUEST, f"Expected {HTTP_STATUS_BAD_REQUEST} status, got {response_missing_login.status_code}"
        assert response_missing_login.json().get(
            "message") == ERROR_MESSAGE_MISSING_COURIER_FIELDS, "Error message doesn't match"

        # Отправляем запрос без пароля
        payload_missing_password = {
            "login": "uniqueLogin123",
            "firstName": "New Courier"
        }
        response_missing_password = requests.post(CREATE_COURIER_URL, json=payload_missing_password)
        assert response_missing_password.status_code == HTTP_STATUS_BAD_REQUEST, f"Expected {HTTP_STATUS_BAD_REQUEST} status, got {response_missing_password.status_code}"
        assert response_missing_password.json().get(
            "message") == ERROR_MESSAGE_MISSING_COURIER_FIELDS, "Error message doesn't match"

    @allure.title("Test courier creation with duplicate login")
    def test_create_courier_duplicate_login(self, create_courier):
        """Тест для проверки ошибки при создании курьера с уже существующим логином."""
        courier_data = create_courier

        duplicate_courier_data = {
            "login": courier_data["login"],
            "password": "newpassword",
            "firstName": "New Courier"
        }

        response = requests.post(CREATE_COURIER_URL, json=duplicate_courier_data)

        print(response.text)

        assert response.status_code == HTTP_STATUS_CONFLICT, f"Expected {HTTP_STATUS_CONFLICT} status, got {response.status_code}"
        assert response.json().get(
            "message") == ERROR_MESSAGE_DUPLICATE_LOGIN, f"Expected error message '{ERROR_MESSAGE_DUPLICATE_LOGIN}', got '{response.json().get('message')}'"
