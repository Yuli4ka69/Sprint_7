import allure
import pytest
from pages.order_api import OrderPage
from data import VALID_ORDER_PAYLOAD


@allure.feature("Order API")
@allure.story("Create Order with different colors")
class TestCreateOrderWithColors:
    """Тесты для создания заказов с различными цветами."""

    @pytest.mark.parametrize(
        "color, missing_field",
        [
            (["BLACK"], None),
            (["GREY"], None),
            (["BLACK", "GREY"], None),
            ([], None),
        ],
    )
    @allure.title("Test creating an order with color: {color}, missing_field: {missing_field}")
    def test_create_order_with_colors(self, color, missing_field):
        """Создание заказа с разными цветами и без поля color."""
        payload = VALID_ORDER_PAYLOAD.copy()

        # Если нужно, удаляем поле color
        if missing_field == "color":
            payload.pop("color", None)
        else:
            payload["color"] = color

        with allure.step(f"Send POST request to create an order with color: {color}"):
            response = OrderPage.create_order(payload)

        with allure.step("Validate response for successful order creation"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
            response_json = response.json()
            assert "track" in response_json, "Expected 'track' in response"
            assert isinstance(response_json["track"], int), "Expected 'track' to be an integer"
