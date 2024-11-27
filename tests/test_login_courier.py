import allure
from unittest.mock import patch, MagicMock
from pages.courier_login_page import CourierLoginPage
import pytest


def create_mock_response(status_code, json_data):
    """Вспомогательная функция для создания мока ответа API."""
    return MagicMock(status_code=status_code, json=lambda: json_data)


@patch('pages.courier_login_page.requests.post')
@allure.feature("Courier Login")
@allure.story("Courier Login Success")
def test_courier_can_login(mock_post, valid_login_payload):
    """Курьер может авторизоваться."""

    with allure.step("Set up mock response for login success"):
        mock_post.return_value = create_mock_response(200, {"id": 12345})

    with allure.step("Attempt to login"):
        response = CourierLoginPage.login(valid_login_payload)

    with allure.step("Validate successful login response"):
        assert response.status_code == 200
        assert response.json().get("id") == 12345


@pytest.mark.parametrize(
    "payload_modification, expected_status, expected_message",
    [
        (lambda payload: payload.pop("login"), 400, "Недостаточно данных для входа"),
        (lambda payload: payload.pop("password"), 400, "Недостаточно данных для входа"),
        (lambda payload: payload.update({"password": "wrong_password"}), 400, "Неверный логин или пароль"),
        (lambda payload: payload.update({"login": "nonexistent_user"}), 404, "Пользователь не найден"),
    ],
)
@patch('pages.courier_login_page.requests.post')
@allure.feature("Courier Login")
@allure.story("Courier Login Edge Cases")
def test_login_edge_cases(mock_post, valid_login_payload, payload_modification, expected_status, expected_message):
    """Обработка ошибок при авторизации."""
    payload_modification(valid_login_payload)

    with allure.step(f"Set up mock response for error case: {expected_message}"):
        mock_post.return_value = create_mock_response(expected_status, {"message": expected_message})

    with allure.step("Attempt to login"):
        response = CourierLoginPage.login(valid_login_payload)

    with allure.step("Validate error message in response"):
        assert response.status_code == expected_status
        assert response.json().get("message") == expected_message


@patch('pages.courier_login_page.requests.post')
@allure.feature("Courier Login")
@allure.story("Courier Login Success")
def test_login_success_returns_id(mock_post, valid_login_payload):
    """Успешный запрос возвращает id."""

    with allure.step("Set up mock response for login success"):
        mock_post.return_value = create_mock_response(200, {"id": 12345})

    with allure.step("Attempt to login"):
        response = CourierLoginPage.login(valid_login_payload)

    with allure.step("Validate successful login response with id"):
        assert response.status_code == 200
        assert response.json().get("id") == 12345
