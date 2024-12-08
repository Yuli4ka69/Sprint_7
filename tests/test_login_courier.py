import pytest
import allure
from pages.courier_api import CourierPage
from data import (
    HTTP_STATUS_OK,
    HTTP_STATUS_BAD_REQUEST,
    HTTP_STATUS_NOT_FOUND,
    ERROR_MESSAGE_BAD_REQUEST,
    ERROR_MESSAGE_NOT_FOUND,
)

@allure.feature("Courier Management")
class TestCourierLogin:
    """Тесты для авторизации курьера."""

    @allure.story("Successful Login")
    @allure.title("Test courier can login successfully")
    def test_courier_can_login(self, setup_and_teardown):
        """Курьер может успешно авторизоваться."""
        valid_login_payload = {
            "login": setup_and_teardown["login"],
            "password": setup_and_teardown["password"]
        }

        with allure.step("Send POST request to login courier"):
            response = CourierPage.login_courier(valid_login_payload)

        with allure.step("Validate successful login response"):
            assert response.status_code == HTTP_STATUS_OK, (
                f"Expected {HTTP_STATUS_OK}, got {response.status_code}"
            )
            response_json = response.json()
            assert "id" in response_json, "Expected 'id' in response"
            assert isinstance(response_json["id"], int), "Expected 'id' to be an integer"

    @allure.story("Courier Login Error Cases")
    @allure.title("Test courier login without login")
    def test_login_without_login(self, setup_and_teardown):
        """Запрос без логина возвращает ошибку."""
        valid_login_payload = {
            "password": setup_and_teardown["password"]
        }

        with allure.step("Send POST request without login"):
            response = CourierPage.login_courier(valid_login_payload)

        with allure.step("Validate response for missing login"):
            assert response.status_code == HTTP_STATUS_BAD_REQUEST, (
                f"Expected {HTTP_STATUS_BAD_REQUEST}, got {response.status_code}"
            )
            response_json = response.json()
            assert response_json.get("message") == ERROR_MESSAGE_BAD_REQUEST, (
                f"Expected message '{ERROR_MESSAGE_BAD_REQUEST}', got '{response_json.get('message')}'"
            )

    @allure.story("Courier Login Error Cases")
    @allure.title("Test courier login without password")
    def test_login_without_password(self, setup_and_teardown):
        """Запрос без пароля возвращает ошибку."""
        valid_login_payload = {
            "login": setup_and_teardown["login"]
        }

        with allure.step("Send POST request without password"):
            response = CourierPage.login_courier(valid_login_payload)

        with allure.step("Validate response for missing password"):
            assert response.status_code == HTTP_STATUS_BAD_REQUEST, (
                f"Expected {HTTP_STATUS_BAD_REQUEST}, got {response.status_code}"
            )
            response_json = response.json()
            assert response_json.get("message") == ERROR_MESSAGE_BAD_REQUEST, (
                f"Expected message '{ERROR_MESSAGE_BAD_REQUEST}', got '{response_json.get('message')}'"
            )

    @allure.story("Courier Login Error Cases")
    @allure.title("Test courier login with incorrect password")
    def test_login_with_incorrect_password(self, setup_and_teardown):
        """Запрос с неправильным паролем возвращает ошибку."""
        valid_login_payload = {
            "login": setup_and_teardown["login"],
            "password": "wrong_password"
        }

        with allure.step("Send POST request with incorrect password"):
            response = CourierPage.login_courier(valid_login_payload)

        with allure.step("Validate response for incorrect password"):
            assert response.status_code == HTTP_STATUS_NOT_FOUND, (
                f"Expected {HTTP_STATUS_NOT_FOUND}, got {response.status_code}"
            )
            response_json = response.json()
            assert response_json.get("message") == ERROR_MESSAGE_NOT_FOUND, (
                f"Expected message '{ERROR_MESSAGE_NOT_FOUND}', got '{response_json.get('message')}'"
            )

    @allure.story("Courier Login Error Cases")
    @allure.title("Test courier login with non-existent user")
    def test_login_with_non_existent_user(self, setup_and_teardown):
        """Запрос с несуществующим пользователем возвращает ошибку."""
        valid_login_payload = {
            "login": "nonexistent_user",
            "password": setup_and_teardown["password"]
        }

        with allure.step("Send POST request with non-existent user"):
            response = CourierPage.login_courier(valid_login_payload)

        with allure.step("Validate response for non-existent user"):
            assert response.status_code == HTTP_STATUS_NOT_FOUND, (
                f"Expected {HTTP_STATUS_NOT_FOUND}, got {response.status_code}"
            )
            response_json = response.json()
            assert response_json.get("message") == ERROR_MESSAGE_NOT_FOUND, (
                f"Expected message '{ERROR_MESSAGE_NOT_FOUND}', got '{response_json.get('message')}'"
            )
