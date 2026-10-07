import pytest

from app import (
    app,
    wallets,
    add_money,
    withdraw_money,
    get_wallet,
    get_transactions
)


def test_add_money():
    result = add_money(100000, 50000)

    print("Add money result:", result)

    assert result == 150000


def test_withdraw_money():
    result = withdraw_money(100000, 30000)

    print("Withdraw result:", result)

    assert result == 70000


def test_add_money_invalid_amount():
    with pytest.raises(ValueError) as error:
        add_money(100000, 0)

    print("Invalid top up result:", error.value)


def test_withdraw_insufficient_balance():
    with pytest.raises(ValueError) as error:
        withdraw_money(10000, 50000)

    print("Insufficient balance result:", error.value)


def test_get_wallet():
    wallets["1"]["balance"] = 100000

    with app.app_context():
        response, status_code = get_wallet("1")
        data = response.get_json()

        print("Get wallet result:", data)
        print("Status code:", status_code)

        assert status_code == 200
        assert data["id"] == "1"
        assert data["balance"] == 100000


def test_get_transactions():
    wallets["1"]["transactions"] = [
        {
            "type": "topup",
            "amount": 50000,
            "balance_after": 150000
        }
    ]

    with app.app_context():
        response, status_code = get_transactions("1")
        data = response.get_json()

        print("Get transactions result:", data)
        print("Status code:", status_code)

        assert status_code == 200
        assert data["wallet_id"] == "1"
        assert len(data["transactions"]) == 1
        assert data["transactions"][0]["type"] == "topup"
        assert data["transactions"][0]["amount"] == 50000