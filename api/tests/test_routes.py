def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Root!"}

def test_msg_endpoint(client):
    response = client.get("/msg")
    assert response.status_code == 200
    assert "Greetings from" in response.json()["message"]

def test_date_endpoint_valid(client):
    response = client.get("/date/US")
    assert response.status_code == 200
    assert response.json()["iso"] == "US"

def test_date_endpoint_invalid(client):
    response = client.get("/date/ZZ")
    assert response.status_code == 400 # Mapped from ValueError

def test_time_endpoint_valid(client):
    response = client.get("/time/US?format=24h")
    assert response.status_code == 200
    assert "hour" in response.json()
    assert response.json()["meridian"] is None
