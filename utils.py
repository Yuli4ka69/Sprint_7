import requests
import random
import string

def generate_random_string(length=10):
    """Генерирует случайную строку из букв нижнего регистра."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def register_new_courier():
    """Регистрирует нового курьера и возвращает его данные (логин, пароль, имя)."""
    # Создаем случайные данные для курьера
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    # Тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # Отправляем запрос
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=payload)

    # Если успешный ответ, возвращаем данные курьера
    if response.status_code == 201:
        return {"login": login, "password": password, "firstName": first_name}

    # Если неуспешно, возвращаем None
    return None
