COURIER_PAYLOAD = {
    "login": "test_login",
    "password": "test_password",
    "firstName": "Test Courier"
}

ORDER_PAYLOAD = {
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

TRACK_RESPONSE = {
    "order": {
        "id": 12345,
        "status": "delivered",
        "courier": {
            "id": 67890,
            "name": "John Doe"
        }
    }
}
