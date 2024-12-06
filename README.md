# Тестирование API для курьеров и заказов

В этом проекте мы тестируем API для системы управления курьерами и заказами. Тесты покрывают такие операции, как создание курьеров, авторизация, удаление курьера, создание заказов, получение заказов без ID курьра.

## Установка

1. Скачайте проект:

```
   git clone https://github.com/your-repository-url.git
   cd your-project-directory
```

2. Создайте виртуальное окружение:

```
python -m venv .venv
```
3. Активируйте виртуальное окружение:

На Linux/MacOS:

```
source .venv/bin/activate
```
На Windows:

```
.venv\Scripts\activate
```
4. Установите зависимости:

```
pip install -r requirements.txt
```
5. Убедитесь, что у вас установлен Allure для отчетности:

```
pip install allure-pytest
```
### Запуск тестов
Чтобы запустить все тесты, используйте команду:

```
pytest
```
Если вы хотите сгенерировать отчет Allure, используйте:

```
pytest --alluredir=target/allure-results
```
Затем откройте отчет:

```
allure serve target/allure-results
```
### Тесты в проекте

1. Создание курьера

- test_create_courier_success — успешное создание курьера.
- test_create_courier_duplicate — попытка создать двух одинаковых курьеров (ошибка).
- test_create_courier_missing_fields — если какого-то поля нет, запрос возвращает ошибку.
- test_create_courier_existing_login — ошибка при создании пользователя с уже существующим логином.

2. Авторизация курьера


- test_courier_can_login — успешная авторизация курьера.
- test_login_edge_cases — обработка ошибок при авторизации:
Отсутствие логина или пароля.
Неверный логин или пароль.
Пользователь не найден.

3. Создание заказа

- test_create_order — создание заказа с разными цветами (черный, серый, оба или без цвета).
- test_create_order_missing_color — создание заказа без указания цвета.
- test_create_order_success — успешное создание заказа с треком.
- 
4. Получение списка заказов


- test_get_orders_without_courier_id — получение всех заказов.
- test_get_orders_with_courier_id — получение заказов с фильтром по courierId.
- test_get_orders_with_parametrized_courier_id — проверка получения заказов с параметризированным courierId.
- test_get_orders_with_limit — проверка ограничения по количеству заказов.


6. Принятие заказа


- test_accept_order — успешное принятие заказа курьером.
- test_accept_order_missing_courier_id — ошибка при отсутствии ID курьера.
- test_accept_order_missing_order_id — ошибка при отсутствии ID заказа.
- test_accept_order_invalid_courier_id — ошибка при неверном ID курьера.
- test_accept_order_invalid_order_id — ошибка при неверном ID заказа.

8. Получение списка заказов


- test_get_all_orders — успешное получение списка заказов без id курьера.

## Структура проекта

- **`pages/`** — классы Page Object для работы с различными API.
  - **`courier_login_page.py`** — взаимодействие с API логина курьера.
  - **`courier_page.py`** — взаимодействие с API курьера.
  - **`order_page.py`** — взаимодействие с API заказов.

- **`tests/`** — тесты для методов API.
  - **`test_accept_order.py`** — тесты для принятия заказов.
  - **`test_create_courier.py`** — тесты для создания курьеров.
  - **`test_create_order.py`** — тесты для создания заказов.
  - **`test_get_order.py`** — тесты для получения заказов по номеру отслеживания.
  - **`test_login_courier.py`** — тесты для авторизации курьеров.
  
- **`target/`** — результаты отчетов Allure.
  - **`allure-results/`** — файлы результатов тестов для генерации отчетов Allure.

- **`conftest.py`** — конфигурация фикстур для тестов.
- **`data.py`** — данные, используемые в тестах.
- **`urls.py`** — содержит базовый URL и эндпоинты для API.
- **`helpers.py`** — вспомогательные функции для мокирования запросов и настройки тестов.
