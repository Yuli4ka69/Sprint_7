import allure
import pytest
from pages.courier_api import CourierPage
from helpers import generate_random_string, register_new_courier


@pytest.fixture(scope="class", autouse=True)
def setup_and_teardown():
    """
    Фикстура для регистрации уникального курьера перед тестами.
    """
    with allure.step("Регистрация уникального курьера перед тестами"):
        courier_data = register_new_courier()
        yield courier_data


@pytest.fixture
def valid_login_payload(setup_and_teardown):
    return {
        "login": setup_and_teardown["login"],
        "password": setup_and_teardown["password"],
    }


@pytest.fixture
def create_courier():
    """Фикстура для создания курьера и получения его ID через авторизацию."""

    # Создаем курьера
    courier_payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }

    # Создаем курьера через API и игнорируем ответ
    CourierPage.create_courier(courier_payload)  # Здесь результат не используется

    # Авторизация курьера для получения ID
    login_payload = {
        "login": courier_payload["login"],
        "password": courier_payload["password"],
    }
    auth_response = CourierPage.login_courier(login_payload)

    courier_id = auth_response.json().get("id")

    # Передаем ID курьера в тесты
    yield courier_id

    # Удаляем курьера после завершения всех тестов
    CourierPage.delete_courier(courier_id)
