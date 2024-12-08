import allure
import requests
from data import HTTP_STATUS_OK
from urls import ORDERS_URL


@allure.feature("Order API")
@allure.story("Get Orders")
class TestGetAllOrders:
    """Тесты для получения списка всех заказов."""

    @allure.title("Test getting all orders without courierId")
    def test_get_all_orders(self):
        """Успешный запрос для получения всех заказов."""
        with allure.step("Send GET request to retrieve all orders"):
            response = requests.get(ORDERS_URL)
            assert response.status_code == HTTP_STATUS_OK, (
                f"Expected {HTTP_STATUS_OK}, got {response.status_code}"
            )

            response_json = response.json()
            allure.attach(str(response_json), name="Response JSON", attachment_type=allure.attachment_type.JSON)

        with allure.step("Validate response contains 'orders' and is a list"):
            assert "orders" in response_json, "'orders' key is missing in the response"
            orders = response_json["orders"]
            assert isinstance(orders, list), "'orders' is not a list"
            assert len(orders) > 0, "Orders list is empty"

        with allure.step("Validate structure of the first order"):
            first_order = orders[0]
            required_keys = [
                "id", "courierId", "firstName", "lastName", "address",
                "metroStation", "phone", "rentTime", "deliveryDate",
                "track", "color", "comment", "createdAt", "updatedAt", "status"
            ]
            for key in required_keys:
                assert key in first_order, f"Key '{key}' is missing in the order"

