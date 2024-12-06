BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

# Courier URLs
COURIER_LOGIN_URL = f"{BASE_URL}/courier/login"  # Логин курьера
CREATE_COURIER_URL = f"{BASE_URL}/courier"  # Создание курьера
DELETE_COURIER_URL = f"{BASE_URL}/courier/{{id}}"  # Удаление курьера

# Orders URLs
ORDERS_URL = f"{BASE_URL}/orders"  # Список заказов
TRACK_ORDER_URL = f"{BASE_URL}/orders/track"  # Получить заказ по номеру
ACCEPT_ORDER_URL = f"{BASE_URL}/orders/accept/{{id}}"  # Принять заказ

# Utils URLs
PING_SERVER_URL = f"{BASE_URL}/ping"  # Проверка доступности сервера
STATIONS_SEARCH_URL = f"{BASE_URL}/stations/search"  # Поиск станций метро
