import allure
import pytest
from pages.courier_api import CourierPage


@pytest.fixture(scope="class")
def setup_and_teardown():
    """
    Фикстура для регистрации уникального курьера перед тестами.
    """
    with allure.step("Регистрация уникального курьера перед тестами"):
        courier_data = CourierPage.register_new_courier()
        yield courier_data


@pytest.fixture(scope="class")  # Устанавливаем scope="class", чтобы фикстура выполнялась один раз на класс
def create_courier():
    """Фикстура для создания курьера и получения его ID через авторизацию."""
    courier_data = CourierPage.register_new_courier()
    assert courier_data is not None, "Courier creation failed"
    assert "id" in courier_data, "Courier ID not found in the response"

    login_payload = {
        "login": courier_data["login"],
        "password": courier_data["password"],
    }

    auth_response = CourierPage.login_courier(login_payload)
    courier_id = auth_response.json().get("id")
    assert courier_id is not None, f"Failed to authorize courier, no ID returned. Response: {auth_response.text}"

    yield courier_data

    # Удаление курьера после выполнения всех тестов
    CourierPage.delete_courier(courier_id)