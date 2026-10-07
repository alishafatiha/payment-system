# Wallet API

A simple REST API for managing digital wallets, built with **Flask**. It supports checking balances, top-ups, withdrawals, and viewing transaction history. Data is stored in memory (a dummy database), which makes it well suited for learning, demos, and practicing unit and integration testing.

## Features

- Check wallet balance
- Top up balance
- Withdraw balance (with sufficient-funds validation)
- View transaction history
- Input validation (`amount` is required, must be a number, and must be greater than 0)
- Unit and integration tests with `pytest`

## Project Structure

```
.
├── app.py                 # Flask app + logic functions (add_money, withdraw_money)
├── test_unit.py           # Unit tests for the logic functions
├── test_integration.py    # Integration tests for the API flow
└── README.md
```

## Prerequisites

Before running the project, make sure Python and pip are installed.
The project uses:

- Flask
- pytest

# TEST ENVIRONMENT

The application and tests were run using the following environment:

- Operating System: macOS
- Python Version: 3.11.5
- Flask
- pytest 9.1.1
- Postman for manual API testing
- VS Code as the code editor

Terminal was used to run the application and execute the tests

Unit tests were executed in the terminal with:
python -m pytest test_unit.py -v -s

Integration tests were executed in the terminal with:
python -m pytest test_integration.py -v -s

## Initial Data

The app ships with two dummy wallets:

| Wallet ID | Initial Balance |
|-----------|----------------:|
| `1`       | 100,000         |
| `2`       | 50,000          |

> **Note:** Data is stored in memory. All changes are lost whenever the server restarts.

## Error Responses

| Status Code | Condition                              | Example Message                 |
|-------------|----------------------------------------|---------------------------------|
| `404`       | Wallet not found                       | `Wallet not found`              |
| `400`       | `amount` field is missing              | `Amount is required`            |
| `400`       | `amount` is not a number               | `Amount must be a number`       |
| `400`       | `amount` is less than or equal to 0    | `Amount must be greater than 0` |
| `400`       | Insufficient balance on withdrawal     | `Insufficient balance`          |

### Test Coverage

**Unit tests** (`test_unit.py`) cover the `add_money` and `withdraw_money` logic functions:

- Adding funds succeeds
- Withdrawing funds succeeds
- Adding an invalid amount (`0`) raises `ValueError`
- Withdrawing with insufficient balance raises `ValueError`

**Integration tests** (`test_integration.py`) cover the full flow through the API:

1. Top up 50,000
2. Withdraw 30,000
3. Check balance
4. Check transaction history

**Manual API testing** was also performed using Postman for:

| Method | Endpoint                     | Description                   |
|--------|------------------------------|-------------------------------|
| GET    | `/wallets/{id}`              | Get wallet balance            |
| POST   | `/wallets/{id}/topup`        | Add funds to a wallet         |
| POST   | `/wallets/{id}/withdraw`     | Withdraw funds from a wallet  |
| GET    | `/wallets/{id}/transactions` | Get transaction history       |

## Test Case Link
[Kunjungi Google](https://google.com)



