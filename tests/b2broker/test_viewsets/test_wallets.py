import pytest
from b2broker.models import Wallet


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_wallet_create(client):
    request = {
        "label": "test_wallet",
    }
    response = client.post("/wallets/", request)
    assert response.status_code == 201
    response_data = response.json()["data"]
    assert response_data["type"] == "wallets"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["label"] == "test_wallet"
    assert response_data["attributes"]["balance"] == "0.0"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_wallet_update(client):
    Wallet.objects.create(label="test_wallet")
    request = {
        "data": {
            "type": "wallets",
            "id": "1",
            "attributes": {
                "label": "test_wallet2",
            },
        }
    }
    response = client.put(
        "/wallets/1/", data=request, content_type="application/vnd.api+json"
    )
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "wallets"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["label"] == "test_wallet2"
    assert response_data["attributes"]["balance"] == "0.0"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_wallet_delete(client):
    w = Wallet.objects.create(label="test_wallet")
    response = client.delete(f"/wallets/{w.id}/")
    assert response.status_code == 204


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_wallet_list(client):
    w = Wallet.objects.create(label="test_wallet")
    response = client.get(f"/wallets/")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 1
    response_data = response.json()["data"]
    assert response_data[0]["type"] == "wallets"
    assert response_data[0]["id"] == "1"
    assert response_data[0]["attributes"]["label"] == "test_wallet"
    assert response_data[0]["attributes"]["balance"] == "0.0"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_wallet_filtering_by_label(client):
    w = Wallet.objects.create(label="test_wallet")
    Wallet.objects.create(label="another_wallet")
    response = client.get(f"/wallets/?filter[label]=test_wallet")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 1
    response_data = response.json()["data"]
    assert response_data[0]["type"] == "wallets"
    assert response_data[0]["id"] == "1"
    assert response_data[0]["attributes"]["label"] == "test_wallet"
    assert response_data[0]["attributes"]["balance"] == "0.0"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_wallet_page_number_pagination(client):
    for i in range(1, 11):
        Wallet.objects.create(label=f"test_wallet{i}")
    response = client.get(f"/wallets/?page[size]=5")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 10
    response_data = response.json()["data"]
    assert len(response_data) == 5
    assert response_data[0]["type"] == "wallets"
    assert response_data[0]["id"] == "1"
    assert response_data[0]["attributes"]["label"] == "test_wallet1"
    assert response_data[4]["type"] == "wallets"
    assert response_data[4]["id"] == "5"
    assert response_data[4]["attributes"]["label"] == "test_wallet5"

    response = client.get(f"/wallets/?page[size]=5&page[number]=2")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 10
    response_data = response.json()["data"]
    assert len(response_data) == 5
    assert response_data[0]["type"] == "wallets"
    assert response_data[0]["id"] == "6"
    assert response_data[0]["attributes"]["label"] == "test_wallet6"
    assert response_data[4]["type"] == "wallets"
    assert response_data[4]["id"] == "10"
    assert response_data[4]["attributes"]["label"] == "test_wallet10"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_wallet_sorting(client):
    for i in range(1, 11):
        Wallet.objects.create(label=f"test_wallet{i}")
    response = client.get(f"/wallets/?sort=label")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 10
    response_data = response.json()["data"]
    assert len(response_data) == 10
    assert response_data[0]["type"] == "wallets"
    assert response_data[0]["id"] == "1"
    assert response_data[0]["attributes"]["label"] == "test_wallet1"
    assert response_data[9]["type"] == "wallets"
    assert response_data[9]["id"] == "9"
    assert response_data[9]["attributes"]["label"] == "test_wallet9"

    response = client.get(f"/wallets/?sort=-label")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 10
    response_data = response.json()["data"]
    assert len(response_data) == 10
    assert response_data[0]["type"] == "wallets"
    assert response_data[0]["id"] == "9"
    assert response_data[0]["attributes"]["label"] == "test_wallet9"
    assert response_data[9]["type"] == "wallets"
    assert response_data[9]["id"] == "1"
    assert response_data[9]["attributes"]["label"] == "test_wallet1"
