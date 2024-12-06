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
    def test_courier_can_login(self, valid_login_payload):
        """Курьер может успешно авторизоваться."""
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
    def test_login_without_login(self, valid_login_payload):
        """Запрос без логина возвращает ошибку."""
        payload = valid_login_payload.copy()
        payload.pop("login", None)

        with allure.step("Send POST request without login"):
            response = CourierPage.login_courier(payload)

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
    def test_login_without_password(self, valid_login_payload):
        """Запрос без пароля возвращает ошибку."""
        payload = valid_login_payload.copy()
        payload.pop("password", None)

        with allure.step("Send POST request without password"):
            response = CourierPage.login_courier(payload)

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
    def test_login_with_incorrect_password(self, valid_login_payload):
        """Запрос с неправильным паролем возвращает ошибку."""
        payload = valid_login_payload.copy()
        payload["password"] = "wrong_password"

        with allure.step("Send POST request with incorrect password"):
            response = CourierPage.login_courier(payload)

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
    def test_login_with_non_existent_user(self, valid_login_payload):
        """Запрос с несуществующим пользователем возвращает ошибку."""
        payload = valid_login_payload.copy()
        payload["login"] = "nonexistent_user"

        with allure.step("Send POST request with non-existent user"):
            response = CourierPage.login_courier(payload)

        with allure.step("Validate response for non-existent user"):
            assert response.status_code == HTTP_STATUS_NOT_FOUND, (
                f"Expected {HTTP_STATUS_NOT_FOUND}, got {response.status_code}"
            )
            response_json = response.json()
            assert response_json.get("message") == ERROR_MESSAGE_NOT_FOUND, (
                f"Expected message '{ERROR_MESSAGE_NOT_FOUND}', got '{response_json.get('message')}'"
            )