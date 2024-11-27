import allure
from unittest.mock import patch, MagicMock
from pages.courier_page import CourierPage


# Тест для создания курьера
@patch('requests.post')
@allure.feature("Courier API")
@allure.story("Create Courier")
def test_create_courier_success(mock_post, valid_courier_payload):
    """Курьера можно создать."""

    # Настройка мока для успешного создания курьера
    mock_post.return_value = MagicMock(
        status_code=201,
        json=lambda: {"ok": True, "id": 123}
    )

    with allure.step("Setup: Mock response for courier creation"):
        pass

    # Создание курьера
    with allure.step(f"Send POST request to create courier with payload: {valid_courier_payload}"):
        response = CourierPage.create_courier(valid_courier_payload)

    # Проверка успешного ответа
    with allure.step(f"Validate response for created courier"):
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        assert response.json() == {"ok": True, "id": 123}, f"Expected {'ok': True, 'id': 123}, got {response.json()}"

    # Проверка вызова mock
    with allure.step("Check that the POST request was called once"):
        mock_post.assert_called_once_with(
            CourierPage.BASE_URL,
            json=valid_courier_payload
        )


# Тест для создания дублирующегося курьера
@patch('requests.post')
@allure.feature("Courier API")
@allure.story("Create Courier Duplicate")
def test_create_courier_duplicate(mock_post, valid_courier_payload):
    """Нельзя создать двух одинаковых курьеров."""

    # Настройка мока для двух вызовов — успешное создание и ошибка при повторном создании
    mock_post.side_effect = [
        MagicMock(status_code=201, json=lambda: {"ok": True, "id": 123}),
        MagicMock(status_code=409, json=lambda: {"message": "Courier already exists"}),
    ]

    with allure.step("Setup: Mock response for first courier creation"):
        pass

    # Первый вызов — создание курьера
    with allure.step(f"Send POST request to create the first courier with payload: {valid_courier_payload}"):
        first_response = CourierPage.create_courier(valid_courier_payload)

    # Проверка первого ответа
    with allure.step("Validate first response"):
        assert first_response.status_code == 201, f"Expected 201, got {first_response.status_code}"
        assert first_response.json() == {"ok": True,
                                         "id": 123}, f"Expected {'ok': True, 'id': 123}, got {first_response.json()}"

    # Второй вызов — создание того же курьера
    with allure.step("Send POST request to create the duplicate courier"):
        second_response = CourierPage.create_courier(valid_courier_payload)

    # Проверка второго ответа (ошибка)
    with allure.step("Validate second response for duplicate courier"):
        assert second_response.status_code == 409, f"Expected 409, got {second_response.status_code}"
        assert second_response.json() == {"message": "Courier already exists"}, \
            f"Expected {'message': 'Courier already exists'}, got {second_response.json()}"

    # Проверка вызова mock
    with allure.step("Check that the POST request was called twice"):
        assert mock_post.call_count == 2
        mock_post.assert_any_call(
            CourierPage.BASE_URL,
            json=valid_courier_payload
        )
