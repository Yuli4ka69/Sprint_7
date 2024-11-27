import allure
from unittest.mock import patch, MagicMock
from pages.order_page import OrderPage


@patch('requests.get')
@allure.feature("Order API")
@allure.story("Get Order by Track Number")
def test_get_order_success(mock_get):
    """Успешный запрос возвращает объект с заказом."""

    with allure.step("Set up mock response with order details"):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"order": "details"})

    track_number = 521394
    with allure.step(f"Send get request for track number {track_number}"):
        response = OrderPage.get_order_by_track(track_number)

    with allure.step("Validate response status code"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Validate response contains order details"):
        assert "order" in response.json(), f"Expected 'order' in response, got {response.json()}"
