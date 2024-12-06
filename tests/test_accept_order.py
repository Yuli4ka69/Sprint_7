import allure
import pytest
from pages.order_api import OrderPage
from data import VALID_ORDER_PAYLOAD


@allure.feature("Order API")
@allure.story("Get order by tracking number")
class TestGetOrderByTrack:
    """Тесты для получения заказа по трек-номеру."""

    @allure.title("Test getting an order by track number successfully")
    def test_get_order_success(self):
        """Проверка успешного запроса на получение заказа по трек-номеру."""
        payload = VALID_ORDER_PAYLOAD.copy()
        payload["color"] = ["BLACK"]

        # Создание нового заказа
        with allure.step("Create a new order"):
            create_response = OrderPage.create_order(payload)
            assert create_response.status_code == 201, "Failed to create order"
            track = create_response.json().get("track")
            assert track, "Track number is missing in the response"

        # Запрос на получение заказа по трек-номеру
        with allure.step("Get the order by track number with retries"):
            responses = [
                OrderPage.get_order_by_track(track)
                for _ in range(10)
            ]

        # Проверка наличия успешного ответа
        response = next(
            (resp for resp in responses if resp.status_code == 200), None
        )
        assert response, f"Order with track {track} was not found within retries."

        # Проверка данных заказа
        with allure.step("Validate the response for the order"):
            response_json = response.json()
            assert "order" in response_json, "Response does not contain 'order'"
            assert response_json["order"]["track"] == track, "Track number does not match"
    @allure.title("Test getting an order with missing track number")
    def test_get_order_without_tracking_number(self):
        """Проверка запроса без трек-номера."""
        with pytest.raises(ValueError, match="Track number is required"):
            OrderPage.get_order_by_track("")

    @allure.title("Test getting a non-existent order")
    def test_get_order_not_found(self):
        """Проверка запроса на получение несуществующего заказа по трек-номеру."""
        non_existent_track_number = 99999999  # Несуществующий трек-номер

        with allure.step(f"Send GET request for non-existent track number {non_existent_track_number}"):
            response = OrderPage.get_order_by_track(non_existent_track_number)

        with allure.step("Validate the response for non-existent order"):
            assert response.status_code == 404, (
                f"Expected 404, got {response.status_code}, Response body: {response.json()}"
            )
            response_json = response.json()
            assert "message" in response_json, "Response does not contain 'message'"
            assert response_json["message"] == "Заказ не найден", (
                f"Expected 'Not Found.', got '{response_json['message']}'"
            )
