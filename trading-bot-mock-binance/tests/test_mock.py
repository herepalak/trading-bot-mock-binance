from bot.mock_client import MockClient
from bot.orders import OrderRequest

def test_market_buy_filled():
    c = MockClient()
    r = c.place_order(OrderRequest(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.001))
    assert r.status == "FILLED"
    assert r.executedQty > 0

def test_limit_resting_when_not_marketable():
    c = MockClient()
    # Buy at an extremely low price to avoid fill
    r = c.place_order(OrderRequest(symbol="BTCUSDT", side="BUY", type="LIMIT", quantity=0.001, price=1.0))
    assert r.status == "NEW"
