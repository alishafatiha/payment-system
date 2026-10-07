import pytest
from app import app, wallets


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_wallet_flow(client):
    # Reset data awal
    wallets["1"]["balance"] = 100000
    wallets["1"]["transactions"] = []

    # 1. Top up
    response = client.post(
        "/wallets/1/topup",
        json={"amount": 50000}
    )

    print("Top up status:", response.status_code)
    print("Top up result:", response.get_json())

    assert response.status_code == 200
    assert response.get_json()["balance"] == 150000


    # 2. Withdraw
    response = client.post(
        "/wallets/1/withdraw",
        json={"amount": 30000}
    )

    print("Withdraw status:", response.status_code)
    print("Withdraw result:", response.get_json())

    assert response.status_code == 200
    assert response.get_json()["balance"] == 120000


    # 3. Check balance
    response = client.get("/wallets/1")

    print("Balance status:", response.status_code)
    print("Balance result:", response.get_json())

    assert response.status_code == 200
    assert response.get_json()["balance"] == 120000


    # 4. Check transaction history
    response = client.get("/wallets/1/transactions")

    data = response.get_json()

    print("Transaction status:", response.status_code)
    print("Transaction result:", data)

    assert response.status_code == 200
    assert len(data["transactions"]) == 2
    assert data["transactions"][0]["type"] == "topup"
    assert data["transactions"][0]["amount"] == 50000
    assert data["transactions"][1]["type"] == "withdraw"
    assert data["transactions"][1]["amount"] == 30000