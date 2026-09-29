from app import app

def test_get_all_customers():
    client = app.test_client()
    response = client.get("/api/customers")
    
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_customer():
    client = app.test_client()
    response = client.get("/api/customers/1")
    
    assert response.status_code == 200
    assert response.json["id"]=="1"

def test_get_customer_not_found():
    client = app.test_client()
    response = client.get("/api/customers/999")
    
    assert response.status_code == 404

def test_create_customer():
    client = app.test_client()
    response = client.post(
        "/api/customers",
        json={
            "id": "100",
            "name": "Test Customer"
            })

    assert response.status_code == 201
    assert response.json["id"]=="100"
    assert response.json["name"]=="Test Customer"

def test_create_customer_missing_data():
    client = app.test_client()
    response = client.post(
        "/api/customers",
        json={
            "id": "101"
            })

    assert response.status_code == 400

def test_update_customer():
    client = app.test_client()
    response = client.put(
        "/api/customers/1",
        json={
            "name": "Updated Customer"
            })

    assert response.status_code == 200
    assert response.json["name"] == "Updated Customer"

def test_update_customer_not_found():
    client = app.test_client()
    response = client.put(
        "/api/customers/999",
        json={"name": "Updated Customer"}
    )
    assert response.status_code == 404

def test_delete_customer():
    client = app.test_client()
    response = client.delete("/api/customers/2")
    assert response.status_code == 200

def test_delete_customer_not_found():
    client = app.test_client()
    response = client.delete("/api/customers/999")
    assert response.status_code == 404
