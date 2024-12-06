import allure
from helpers import generate_random_string
from pages.courier_api import CourierPage
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
        courier_id = create_courier
        assert courier_id is not None, "Courier ID should not be None after successful creation"

    @allure.title("Test courier creation with duplicate payload")
    def test_create_courier_duplicate(self, create_courier):
        """Нельзя создать двух одинаковых курьеров."""
        valid_courier_payload = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string(),
        }
        CourierPage.create_courier(valid_courier_payload)
        response = CourierPage.create_courier(valid_courier_payload)
        assert response.status_code == HTTP_STATUS_CONFLICT, f"Expected {HTTP_STATUS_CONFLICT}, got {response.status_code}"

        assert response.json()["message"] == f"{ERROR_MESSAGE_DUPLICATE_LOGIN}.", (
            f"Expected message: {ERROR_MESSAGE_DUPLICATE_LOGIN}., got {response.json()['message']}"
        )

    @allure.title("Test courier creation with missing fields")
    def test_create_courier_missing_fields(self):
        """Проверка создания курьера без обязательных полей."""
        required_fields = ["login", "password"]
        for field in required_fields:
            invalid_payload = {
                "login": generate_random_string(),
                "password": generate_random_string(),
            }
            invalid_payload.pop(field)
            response = CourierPage.create_courier(invalid_payload)

            assert response.status_code == HTTP_STATUS_BAD_REQUEST, (
                f"Expected {HTTP_STATUS_BAD_REQUEST}, got {response.status_code}"
            )
            assert response.json()["message"] == ERROR_MESSAGE_MISSING_COURIER_FIELDS, (
                f"Expected message '{ERROR_MESSAGE_MISSING_COURIER_FIELDS}', got '{response.json()['message']}'"
            )

    @allure.title("Test creating courier with duplicate login")
    def test_create_courier_duplicate_login(self, create_courier):
        """Нельзя создать курьера с уже существующим логином."""
        valid_courier_payload = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string(),
        }
        CourierPage.create_courier(valid_courier_payload)
        response = CourierPage.create_courier(valid_courier_payload)
        assert response.status_code == HTTP_STATUS_CONFLICT, f"Expected {HTTP_STATUS_CONFLICT}, got {response.status_code}"
        assert response.json()["message"] == f"{ERROR_MESSAGE_DUPLICATE_LOGIN}.", (
            f"Expected message: {ERROR_MESSAGE_DUPLICATE_LOGIN}., got {response.json()['message']}"
        )

