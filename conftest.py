import random
import string
import pytest
import requests
from unittest.mock import patch


def generate_random_string(length=10):
    """Генерирует случайную строку из букв нижнего регистра."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


@pytest.fixture
def valid_login_payload():
    """Создает данные для логина курьера."""
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": "Test Courier"
    }


@pytest.fixture
def valid_order_payload():
    """Создает данные для заказа."""
    return {
        "firstName": "Test",
        "lastName": "Order",
        "address": "Test Address",
        "metroStation": "4",
        "phone": "+1234567890",
        "rentTime": 5,
        "deliveryDate": "2024-12-01",
        "comment": "Test comment",
        "color": ["BLACK"]
    }


@pytest.fixture
def valid_courier_payload():
    """Создает данные для курьера через регистрацию API и возвращает их с id."""
    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }

    # Мокаем запрос на регистрацию курьера
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": 123}  # Мокируем ответ с id

        # Отправляем запрос на регистрацию курьера
        response = mock_post('https://example.com/courier', json=payload)  # Используем мок
        # Проверяем успешность регистрации
        assert response.status_code == 201, f"Failed to register courier, got {response.status_code}"
        assert "id" in response.json(), "Response does not contain 'id'"

        # Возвращаем payload с id
        payload["id"] = response.json()["id"]

    return payload

@pytest.fixture
def mock_orders_response():
    """Возвращает мок для списка заказов."""
    return {
        "orders": [
            {
                "id": 4,
                "courierId": None,
                "firstName": "Иван",
                "lastName": "Иванов",
                "address": "Москва, Тверская, 1",
                "metroStation": "1",
                "phone": "+7 900 123 45 67",
                "rentTime": 5,
                "deliveryDate": "2024-12-01T00:00:00.000Z",
                "track": 123456,
                "color": ["BLACK"],
                "comment": "Срочная доставка",
                "createdAt": "2024-11-25T13:00:00.000Z",
                "updatedAt": "2024-11-25T14:00:00.000Z",
                "status": 0
            }
        ],
        "pageInfo": {"page": 0, "total": 1, "limit": 30},
        "availableStations": []
    }


@pytest.fixture
def order_payload():
    """Создает данные для заказа с рандомными значениями."""
    return {
        "firstName": generate_random_string(),
        "lastName": generate_random_string(),
        "address": f"{generate_random_string()} Street, 123",
        "metroStation": "4",
        "phone": "+7 800 555 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-11-30",
        "comment": "Please be quick",
        "color": []
    }


@pytest.fixture
def mock_delete_response():
    """Возвращает мок для ответа удаления курьера."""
    return {
        "ok": True
    }

@pytest.fixture
def mock_put_request():
    """Фикстура для настройки мока PUT-запроса."""
    with patch('requests.put') as mock_put:
        yield mock_put


@pytest.fixture
def mock_successful_get_order_response():
    """Возвращает мок для успешного запроса с заказом."""
    return {
        "id": 1,
        "courierId": 123,
        "firstName": "Test",
        "lastName": "Order",
        "address": "Test Address",
        "status": "Pending"
    }

@pytest.fixture
def mock_missing_order_id_response():
    """Возвращает мок для ошибки, если не передан номер заказа."""
    return {"message": "Order ID is required"}

@pytest.fixture
def mock_not_found_order_response():
    """Возвращает мок для ошибки, если заказ не найден."""
    return {"message": "Order not found"}
