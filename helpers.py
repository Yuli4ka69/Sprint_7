import requests
from urls import CREATE_COURIER_URL
import random
import string


def generate_random_string(length=10):
    """Генерирует случайную строку из букв нижнего регистра."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def register_new_courier():
    """Регистрирует нового курьера и возвращает его данные (логин, пароль, имя)."""
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(CREATE_COURIER_URL, json=payload)
    if response.status_code == 201:
        return payload
    return None
