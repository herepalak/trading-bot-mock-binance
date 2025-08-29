from .client import ExchangeClient
from .orders import OrderRequest, OrderResponse, gen_order_id, now_ms
import random

class MockClient(ExchangeClient):
    def __init__(self):
        self._last_price = {"BTCUSDT": 70000.0, "ETHUSDT": 3500.0}

    def mode(self) -> str:
        return "mock"

    def _mark_price(self, symbol: str) -> float:
        base = self._last_price.get(symbol, 100.0)
        # random walk for fun
        change = random.uniform(-0.5, 0.5)
        newp = max(1.0, base + change)
        self._last_price[symbol] = newp
        return newp

    def place_order(self, req: OrderRequest) -> OrderResponse:
        req.validate()
        mark = self._mark_price(req.symbol)
        order_id = gen_order_id()
        status = "NEW"
        executed = 0.0
        fill_price = None

        if req.type == "MARKET":
            status = "FILLED"
            executed = float(req.quantity)
            fill_price = mark
        elif req.type == "LIMIT":
            # Fill immediately if price is marketable (BUY price >= mark or SELL price <= mark)
            is_buy = req.side == "BUY"
            marketable = (req.price >= mark) if is_buy else (req.price <= mark)
            if marketable:
                status = "FILLED"
                executed = float(req.quantity)
                fill_price = req.price
            else:
                status = "NEW"  # resting
                fill_price = req.price
        elif req.type == "STOP_LIMIT":
            # Trigger when mark crosses stopPrice, then place limit at req.price
            if (req.side == "BUY" and mark >= req.stopPrice) or (req.side == "SELL" and mark <= req.stopPrice):
                # On trigger, assume immediate execution at limit
                status = "FILLED"
                executed = float(req.quantity)
                fill_price = req.price
            else:
                status = "NEW"
                fill_price = req.price

        return OrderResponse(
            symbol=req.symbol,
            side=req.side,
            type=req.type,
            status=status,
            orderId=order_id,
            transactTime=now_ms(),
            price=fill_price,
            origQty=float(req.quantity),
            executedQty=executed,
            clientOrderId=req.clientOrderId or order_id[:12],
            extra={"markPrice": mark}
        )
