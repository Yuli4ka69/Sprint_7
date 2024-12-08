import allure
from pages.order_api import OrderPage
from data import VALID_ORDER_PAYLOAD


@allure.feature("Order API")
@allure.story("Create Order with different payload configurations")
class TestCreateOrder:
    """Тесты для создания заказов с различными вариантами payload."""

    @allure.title("Test creating an order with color BLACK")
    def test_create_order_with_black_color(self):
        """Создание заказа с цветом BLACK."""
        payload = VALID_ORDER_PAYLOAD.copy()
        payload["color"] = ["BLACK"]

        with allure.step("Send POST request to create an order with color BLACK"):
            response = OrderPage.create_order(payload)

        with allure.step("Validate response for successful order creation"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
            response_json = response.json()
            assert "track" in response_json, "Expected 'track' in response"
            assert isinstance(response_json["track"], int), "Expected 'track' to be an integer"

    @allure.title("Test creating an order with color GREY")
    def test_create_order_with_grey_color(self):
        """Создание заказа с цветом GREY."""
        payload = VALID_ORDER_PAYLOAD.copy()
        payload["color"] = ["GREY"]

        with allure.step("Send POST request to create an order with color GREY"):
            response = OrderPage.create_order(payload)

        with allure.step("Validate response for successful order creation"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
            response_json = response.json()
            assert "track" in response_json, "Expected 'track' in response"
            assert isinstance(response_json["track"], int), "Expected 'track' to be an integer"

    @allure.title("Test creating an order with colors BLACK and GREY")
    def test_create_order_with_black_and_grey_colors(self):
        """Создание заказа с цветами BLACK и GREY."""
        payload = VALID_ORDER_PAYLOAD.copy()
        payload["color"] = ["BLACK", "GREY"]

        with allure.step("Send POST request to create an order with colors BLACK and GREY"):
            response = OrderPage.create_order(payload)

        with allure.step("Validate response for successful order creation"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
            response_json = response.json()
            assert "track" in response_json, "Expected 'track' in response"
            assert isinstance(response_json["track"], int), "Expected 'track' to be an integer"

    @allure.title("Test creating an order with no colors")
    def test_create_order_with_no_colors(self):
        """Создание заказа без указания цветов."""
        payload = VALID_ORDER_PAYLOAD.copy()
        payload["color"] = []

        with allure.step("Send POST request to create an order with no colors"):
            response = OrderPage.create_order(payload)

        with allure.step("Validate response for successful order creation"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
            response_json = response.json()
            assert "track" in response_json, "Expected 'track' in response"
            assert isinstance(response_json["track"], int), "Expected 'track' to be an integer"

    @allure.title("Test creating an order without color field")
    def test_create_order_without_color_field(self):
        """Создание заказа без поля color."""
        payload = VALID_ORDER_PAYLOAD.copy()
        payload.pop("color", None)

        with allure.step("Send POST request to create an order without color field"):
            response = OrderPage.create_order(payload)

        with allure.step("Validate response for successful order creation"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
            response_json = response.json()
            assert "track" in response_json, "Expected 'track' in response"
            assert isinstance(response_json["track"], int), "Expected 'track' to be an integer"
