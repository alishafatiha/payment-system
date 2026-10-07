from flask import Flask, request, jsonify

app = Flask(__name__)


# =========================
# Dummy Database
# =========================

wallets = {
    "1": {
        "balance": 100000,
        "transactions": []
    },
    "2": {
        "balance": 50000,
        "transactions": []
    }
}

# Fungsi fungsi unit logic
def add_money(balance, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    return balance + amount


def withdraw_money(balance, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    if balance < amount:
        raise ValueError("Insufficient balance")

    return balance - amount


# =========================
# Helper Function
# =========================

def validate_amount(data):
    if not data or "amount" not in data:
        return None, "Amount is required"

    amount = data["amount"]

    if not isinstance(amount, (int, float)):
        return None, "Amount must be a number"

    if amount <= 0:
        return None, "Amount must be greater than 0"

    return amount, None


# =========================
# GET BALANCE
# GET /wallets/{id}
# =========================

@app.route("/wallets/<id>", methods=["GET"])
def get_wallet(id):
    wallet = wallets.get(id)

    if not wallet:
        return jsonify({
            "error": "Wallet not found"
        }), 404

    return jsonify({
        "id": id,
        "balance": wallet["balance"]
    }), 200


# =========================
# TOP UP
# POST /wallets/{id}/topup
# =========================

@app.route("/wallets/<id>/topup", methods=["POST"])
def topup(id):
    wallet = wallets.get(id)

    if not wallet:
        return jsonify({
            "error": "Wallet not found"
        }), 404

    data = request.get_json()

    amount, error = validate_amount(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    wallet["balance"] += amount

    wallet["transactions"].append({
        "type": "topup",
        "amount": amount,
        "balance_after": wallet["balance"]
    })

    return jsonify({
        "message": "Top up successful",
        "balance": wallet["balance"]
    }), 200


# =========================
# WITHDRAW
# POST /wallets/{id}/withdraw
# =========================

@app.route("/wallets/<id>/withdraw", methods=["POST"])
def withdraw(id):
    wallet = wallets.get(id)

    if not wallet:
        return jsonify({
            "error": "Wallet not found"
        }), 404

    data = request.get_json()

    amount, error = validate_amount(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    if wallet["balance"] < amount:
        return jsonify({
            "error": "Insufficient balance"
        }), 400

    wallet["balance"] -= amount

    wallet["transactions"].append({
        "type": "withdraw",
        "amount": amount,
        "balance_after": wallet["balance"]
    })

    return jsonify({
        "message": "Withdraw successful",
        "balance": wallet["balance"]
    }), 200


# =========================
# TRANSACTION HISTORY
# GET /wallets/{id}/transactions
# =========================

@app.route("/wallets/<id>/transactions", methods=["GET"])
def get_transactions(id):
    wallet = wallets.get(id)

    if not wallet:
        return jsonify({
            "error": "Wallet not found"
        }), 404

    return jsonify({
        "wallet_id": id,
        "transactions": wallet["transactions"]
    }), 200


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(debug=True)