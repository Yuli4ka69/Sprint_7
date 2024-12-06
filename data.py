# Тестовые данные для получения информации о заказе
VALID_ORDER_PAYLOAD = {
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

HEADERS = {
    "Content-Type": "application/json"
}

# Ожидаемые сообщения об ошибках
ERROR_MESSAGE_NOT_FOUND = "Учетная запись не найдена"
ERROR_MESSAGE_BAD_REQUEST = "Недостаточно данных для входа"
ERROR_MESSAGE_MISSING_COURIER_FIELDS = "Недостаточно данных для создания учетной записи"
ERROR_MESSAGE_DUPLICATE_LOGIN = "Этот логин уже используется. Попробуйте другой"

# Ожидаемые статусы для различных сценариев
HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_BAD_REQUEST = 400  # только статус 400 для некорректных запросов
HTTP_STATUS_NOT_FOUND = 404   # статус 404 для "не найдено"
HTTP_STATUS_CONFLICT = 409     # статус 409 для конфликтов, например, дублирование данных
