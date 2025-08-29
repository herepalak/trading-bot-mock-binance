from dataclasses import dataclass, asdict
from typing import Optional, Literal, Dict, Any
import uuid, time

Side = Literal["BUY", "SELL"]
OrderType = Literal["MARKET", "LIMIT", "STOP_LIMIT"]

@dataclass
class OrderRequest:
    symbol: str
    side: Side
    type: OrderType
    quantity: float
    price: Optional[float] = None
    stopPrice: Optional[float] = None
    clientOrderId: Optional[str] = None

    def validate(self):
        if not self.symbol or not isinstance(self.symbol, str):
            raise ValueError("symbol is required")
        if self.side not in ("BUY","SELL"):
            raise ValueError("side must be BUY or SELL")
        if self.type not in ("MARKET","LIMIT","STOP_LIMIT"):
            raise ValueError("type must be MARKET, LIMIT, or STOP_LIMIT")
        if self.quantity is None or self.quantity <= 0:
            raise ValueError("quantity must be > 0")
        if self.type == "LIMIT" and (self.price is None or self.price <= 0):
            raise ValueError("price is required for LIMIT")
        if self.type == "STOP_LIMIT":
            if self.price is None or self.price <= 0:
                raise ValueError("price is required for STOP_LIMIT")
            if self.stopPrice is None or self.stopPrice <= 0:
                raise ValueError("stopPrice is required for STOP_LIMIT")

@dataclass
class OrderResponse:
    symbol: str
    side: Side
    type: OrderType
    status: str
    orderId: str
    transactTime: int
    price: Optional[float] = None
    origQty: float = 0.0
    executedQty: float = 0.0
    clientOrderId: Optional[str] = None
    extra: Dict[str, Any] = None

    def to_dict(self):
        d = asdict(self)
        if self.extra is None:
            d.pop("extra")
        return d

def gen_order_id() -> str:
    return uuid.uuid4().hex[:24]

def now_ms() -> int:
    return int(time.time() * 1000)
