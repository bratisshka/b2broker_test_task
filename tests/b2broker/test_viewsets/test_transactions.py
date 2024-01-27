import pytest
from b2broker.models import Wallet, Transaction


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_create(client):
    w = Wallet.objects.create(label="test_wallet")
    request = {
        "data": {
            "type": "transactions",
            "attributes": {
                "txid": "123",
                "amount": "10",
            },
            "relationships": {"wallet": {"data": {"type": "wallets", "id": "1"}}},
        }
    }
    response = client.post(
        "/transactions/", data=request, content_type="application/vnd.api+json"
    )
    assert response.status_code == 201
    response_data = response.json()["data"]
    assert response_data["type"] == "transactions"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["txid"] == "123"
    assert response_data["attributes"]["amount"] == "10.000000000000000000"
    assert response_data["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data["relationships"]["wallet"]["data"]["id"] == "1"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_update(client):
    w = Wallet.objects.create(label="test_wallet")
    t = Transaction.objects.create(
        wallet=w,
        txid="123",
        amount=10,
    )
    request = {
        "data": {
            "type": "transactions",
            "id": "1",
            "attributes": {
                "txid": "123",
                "amount": "20",
            },
            "relationships": {"wallet": {"data": {"type": "wallets", "id": "1"}}},
        }
    }
    response = client.put(
        "/transactions/1/", data=request, content_type="application/vnd.api+json"
    )
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "transactions"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["txid"] == "123"
    assert response_data["attributes"]["amount"] == "20.000000000000000000"
    assert response_data["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data["relationships"]["wallet"]["data"]["id"] == "1"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_update_wallet(client):
    w = Wallet.objects.create(label="test_wallet")
    w2 = Wallet.objects.create(label="test_wallet2")
    t = Transaction.objects.create(
        wallet=w,
        txid="123",
        amount=10,
    )
    # check wallet balance before update
    response = client.get("/wallets/1/")
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "wallets"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["label"] == "test_wallet"
    assert response_data["attributes"]["balance"] == "10.000000000000000000"

    request = {
        "data": {
            "type": "transactions",
            "id": "1",
            "attributes": {
                "txid": "123",
                "amount": "20",
            },
            "relationships": {"wallet": {"data": {"type": "wallets", "id": "2"}}},
        }
    }
    response = client.put(
        "/transactions/1/", data=request, content_type="application/vnd.api+json"
    )
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "transactions"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["txid"] == "123"
    assert response_data["attributes"]["amount"] == "20.000000000000000000"
    assert response_data["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data["relationships"]["wallet"]["data"]["id"] == "2"

    response = client.get("/wallets/1/")
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "wallets"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["label"] == "test_wallet"
    assert response_data["attributes"]["balance"] == "0.0"

    response = client.get("/wallets/2/")
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "wallets"
    assert response_data["id"] == "2"
    assert response_data["attributes"]["label"] == "test_wallet2"
    assert response_data["attributes"]["balance"] == "20.000000000000000000"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_delete(client):
    w = Wallet.objects.create(label="test_wallet")
    t = Transaction.objects.create(
        wallet=w,
        txid="123",
        amount=10,
    )
    # check wallet balance before delete
    response = client.get("/wallets/1/")
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "wallets"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["label"] == "test_wallet"
    assert response_data["attributes"]["balance"] == "10.000000000000000000"

    response = client.delete(f"/transactions/{t.id}/")
    assert response.status_code == 204
    # check wallet balance after delete
    response = client.get("/wallets/1/")
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "wallets"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["label"] == "test_wallet"
    assert response_data["attributes"]["balance"] == "0.0"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_list(client):
    w = Wallet.objects.create(label="test_wallet")
    Transaction.objects.create(
        wallet=w,
        txid="123",
        amount=10,
    )
    response = client.get(f"/transactions/")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 1
    response_data = response.json()["data"]
    assert response_data[0]["type"] == "transactions"
    assert response_data[0]["id"] == "1"
    assert response_data[0]["attributes"]["txid"] == "123"
    assert response_data[0]["attributes"]["amount"] == "10.000000000000000000"
    assert response_data[0]["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data[0]["relationships"]["wallet"]["data"]["id"] == "1"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_filtering_by_txid(client):
    w = Wallet.objects.create(label="test_wallet")
    Transaction.objects.create(
        wallet=w,
        txid="123",
        amount=10,
    )
    Transaction.objects.create(
        wallet=w,
        txid="124",
        amount=10,
    )
    response = client.get(f"/transactions/?filter[txid]=123")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 1
    response_data = response.json()["data"]
    assert response_data[0]["type"] == "transactions"
    assert response_data[0]["id"] == "1"
    assert response_data[0]["attributes"]["txid"] == "123"
    assert response_data[0]["attributes"]["amount"] == "10.000000000000000000"
    assert response_data[0]["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data[0]["relationships"]["wallet"]["data"]["id"] == "1"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_filtering_by_wallet(client):
    w = Wallet.objects.create(label="test_wallet")
    w2 = Wallet.objects.create(label="test_wallet2")
    Transaction.objects.create(
        wallet=w,
        txid="123",
        amount=10,
    )
    Transaction.objects.create(
        wallet=w2,
        txid="124",
        amount=10,
    )
    response = client.get(f"/transactions/?filter[wallet]=1")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 1
    response_data = response.json()["data"]
    assert response_data[0]["type"] == "transactions"
    assert response_data[0]["id"] == "1"
    assert response_data[0]["attributes"]["txid"] == "123"
    assert response_data[0]["attributes"]["amount"] == "10.000000000000000000"
    assert response_data[0]["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data[0]["relationships"]["wallet"]["data"]["id"] == "1"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_page_number_pagination(client):
    w = Wallet.objects.create(label="test_wallet")
    for i in range(1, 11):
        Transaction.objects.create(
            wallet=w,
            txid=f"transaction_{i}",
            amount=10 * i,
        )
    response = client.get(f"/transactions/?page[size]=5")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 10
    response_data = response.json()["data"]
    assert len(response_data) == 5
    assert response_data[0]["type"] == "transactions"
    assert response_data[0]["id"] == "1"
    assert response_data[0]["attributes"]["txid"] == "transaction_1"
    assert response_data[0]["attributes"]["amount"] == "10.000000000000000000"
    assert response_data[4]["type"] == "transactions"
    assert response_data[4]["id"] == "5"
    assert response_data[4]["attributes"]["txid"] == "transaction_5"
    assert response_data[4]["attributes"]["amount"] == "50.000000000000000000"

    response = client.get(f"/transactions/?page[size]=5&page[number]=2")
    assert response.status_code == 200
    assert response.json()["meta"]["pagination"]["count"] == 10
    response_data = response.json()["data"]
    assert len(response_data) == 5
    assert response_data[0]["type"] == "transactions"
    assert response_data[0]["id"] == "6"
    assert response_data[0]["attributes"]["txid"] == "transaction_6"
    assert response_data[0]["attributes"]["amount"] == "60.000000000000000000"
    assert response_data[4]["type"] == "transactions"
    assert response_data[4]["id"] == "10"
    assert response_data[4]["attributes"]["txid"] == "transaction_10"
    assert response_data[4]["attributes"]["amount"] == "100.000000000000000000"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_amount_precision_create_and_retrieve(client):
    Wallet.objects.create(label="test_wallet")
    request = {
        "data": {
            "type": "transactions",
            "attributes": {
                "txid": "123",
                "amount": "10.000000000000000001",
            },
            "relationships": {"wallet": {"data": {"type": "wallets", "id": "1"}}},
        }
    }
    response = client.post(
        "/transactions/", data=request, content_type="application/vnd.api+json"
    )
    assert response.status_code == 201
    response_data = response.json()["data"]
    assert response_data["type"] == "transactions"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["txid"] == "123"
    assert response_data["attributes"]["amount"] == "10.000000000000000001"
    assert response_data["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data["relationships"]["wallet"]["data"]["id"] == "1"

    response = client.get("/transactions/1/")
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "transactions"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["txid"] == "123"
    assert response_data["attributes"]["amount"] == "10.000000000000000001"
    assert response_data["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data["relationships"]["wallet"]["data"]["id"] == "1"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_unique_txid(client):
    w = Wallet.objects.create(label="test_wallet")
    Transaction.objects.create(
        wallet=w,
        txid="123",
        amount=10,
    )
    request = {
        "data": {
            "type": "transactions",
            "attributes": {
                "txid": "123",
                "amount": "10",
            },
            "relationships": {"wallet": {"data": {"type": "wallets", "id": "1"}}},
        }
    }
    response = client.post(
        "/transactions/", data=request, content_type="application/vnd.api+json"
    )
    assert response.status_code == 400
    assert (
            response.json()["errors"][0]["detail"]
            == "transaction with this txid already exists."
    )


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_transaction_amount_can_be_optional(client):
    Wallet.objects.create(label="test_wallet")
    request = {
        "data": {
            "type": "transactions",
            "attributes": {
                "txid": "123",
            },
            "relationships": {"wallet": {"data": {"type": "wallets", "id": "1"}}},
        }
    }
    response = client.post(
        "/transactions/", data=request, content_type="application/vnd.api+json"
    )
    assert response.status_code == 201
    response_data = response.json()["data"]
    assert response_data["type"] == "transactions"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["txid"] == "123"
    assert response_data["attributes"]["amount"] == "0.000000000000000000"
    assert response_data["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data["relationships"]["wallet"]["data"]["id"] == "1"

    response = client.get("/transactions/1/")
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert response_data["type"] == "transactions"
    assert response_data["id"] == "1"
    assert response_data["attributes"]["txid"] == "123"
    assert response_data["attributes"]["amount"] == "0.000000000000000000"
    assert response_data["relationships"]["wallet"]["data"]["type"] == "wallets"
    assert response_data["relationships"]["wallet"]["data"]["id"] == "1"
