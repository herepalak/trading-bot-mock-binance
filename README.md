# Simplified Trading Bot (Binance Futures Testnet) — Mock Mode Ready

This project implements a CLI-based crypto trading bot per the task document. It supports **market** and **limit** orders (buy/sell) using the Binance Futures Testnet via `python-binance` **or** a fully offline **mock mode** that simulates exchange behavior when APIs are unavailable.

## Features
- Market and limit orders (BUY/SELL) for USDT-M futures symbols (e.g., `BTCUSDT`).
- Testnet (real) mode using `python-binance` (optional) and the Futures Testnet base URL.
- **Mock mode** (default if API keys missing or `--mode mock`) — no internet required.
- Input validation via CLI arguments.
- Structured logging of requests/responses/errors to `logs/trading.log`.
- Extensible design: add advanced order types (Stop-Limit scaffold included).
- Simple test for the mock client.

## Project Structure
```
bot/
  __init__.py
  cli.py              # CLI entrypoint
  config.py           # Config/env handling
  logger.py           # Logging setup (RotatingFileHandler)
  orders.py           # Order dataclasses & validation
  client.py           # Abstract client interface
  mock_client.py      # Offline simulation client
  binance_client.py   # Real client wrapper (optional python-binance)
logs/
  trading.log         # created at runtime
tests/
  test_mock.py
requirements.txt
README.md
```

## Quick Start (Mock Mode — works offline)
```bash
# 1) Create virtualenv (recommended)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install deps (python-binance is optional; mock mode needs only stdlib)
pip install -r requirements.txt

# 3) Run a market BUY
python -m bot.cli place --symbol BTCUSDT --side BUY --type MARKET --qty 0.001 --mode mock

# 4) Run a limit SELL
python -m bot.cli place --symbol BTCUSDT --side SELL --type LIMIT --qty 0.002 --price 80000 --mode mock
```

You will see structured logs in `logs/trading.log` and JSON output in the terminal (`status`, `orderId`, etc.).

## Testnet (Real) Mode (optional)
1. Register and activate a **Binance Futures Testnet** account.
2. Create API key/secret.
3. Set environment variables:
   ```bash
   export BINANCE_API_KEY="your_key"
   export BINANCE_API_SECRET="your_secret"
   export BINANCE_TESTNET="true"
   ```
4. Install python-binance and run without `--mode mock`:
   ```bash
   pip install -r requirements.txt
   python -m bot.cli place --symbol BTCUSDT --side BUY --type MARKET --qty 0.001
   ```

> Note: In environments without internet or when the API is down, use `--mode mock`.

## CLI Usage
```
python -m bot.cli place --symbol SYMBOL --side {BUY,SELL} --type {MARKET,LIMIT,STOP_LIMIT} --qty FLOAT [--price FLOAT] [--stopPrice FLOAT] [--mode {auto,mock,real}] [--clientOrderId STR]
```
- `--mode auto` (default): uses real if keys present & library available; otherwise mock.
- Limit orders require `--price`.
- Stop-Limit (scaffold): requires `--stopPrice` and `--price` (mock behavior included).

## Logs
- File: `logs/trading.log` (rotating, max 1 MB × 3)
- Console: INFO+
- Entries capture request params, responses, and errors.

## Running Tests
```bash
pytest -q
```

## Notes
- Symbols and precision are minimally validated in mock mode. Real mode defers to Binance API.
- Extend `mock_client.py` to simulate fills based on a price feed or random walk if desired.
