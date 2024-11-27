import allure
import pytest
from unittest.mock import patch, MagicMock
from pages.order_page import OrderPage


def setup_mock_response(mock_method, status_code, response_json):
    """Универсальный метод настройки мока."""
    mock_method.return_value = MagicMock(
        status_code=status_code,
        json=lambda: response_json
    )


@pytest.mark.parametrize("color, expected_track", [
    (["BLACK"], 124124),  # Один цвет
    (["GREY"], 124124),  # Другой цвет
    (["BLACK", "GREY"], 124124),  # Оба цвета
    ([], 124124),  # Без указания цвета
    (None, 124124)  # Поле color отсутствует
])
@patch('requests.post')
@allure.feature("Order API")
@allure.story("Create Order with different colors")
def test_create_order(mock_post, order_payload, color, expected_track):
    """Проверка создания заказа с различными цветами или без них."""

    # Копируем данные для создания заказа
    payload = order_payload.copy()

    with allure.step("Setup payload with colors or without colors"):
        if color is not None:
            payload["color"] = color
        else:
            payload.pop("color", None)

    # Настроим мок для успешного ответа
    with allure.step(f"Setup mock response with track: {expected_track}"):
        setup_mock_response(mock_post, 201, {"track": expected_track})

    # Отправка запроса на создание заказа
    with allure.step("Send POST request to create the order"):
        response = OrderPage.create_order(payload)

    # Проверка статуса ответа
    with allure.step(f"Validate response status code is 201"):
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Проверка наличия track в ответе
    with allure.step(f"Validate response contains 'track' and it matches the expected value"):
        assert response.json().get("track") == expected_track, (
            f"Expected 'track': {expected_track}, got {response.json()}"
        )
