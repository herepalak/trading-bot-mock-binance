from abc import ABC, abstractmethod
from typing import Optional
from .orders import OrderRequest, OrderResponse

class ExchangeClient(ABC):
    @abstractmethod
    def place_order(self, req: OrderRequest) -> OrderResponse:
        ...

    @abstractmethod
    def mode(self) -> str:
        ...

def choose_client(mode: str, settings):
    mode = (mode or "auto").lower()
    if mode == "mock":
        from .mock_client import MockClient
        return MockClient()
    if mode == "real":
        from .binance_client import BinanceClient
        return BinanceClient(settings)
    # auto
    if settings and settings.has_keys():
        try:
            from .binance_client import BinanceClient
            return BinanceClient(settings)
        except Exception:
            from .mock_client import MockClient
            return MockClient()
    else:
        from .mock_client import MockClient
        return MockClient()
