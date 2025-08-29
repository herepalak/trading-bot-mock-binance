from .client import ExchangeClient
from .orders import OrderRequest, OrderResponse, now_ms, gen_order_id
from .logger import setup_logger
from binance.client import Client as BClient
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET, TIME_IN_FORCE_GTC, ORDER_TYPE_LIMIT, ORDER_TYPE_STOP_LOSS_LIMIT
from binance.exceptions import BinanceAPIException, BinanceRequestException

class BinanceClient(ExchangeClient):
    def __init__(self, settings):
        self.log = setup_logger()
        self.settings = settings
        self.client = BClient(settings.api_key, settings.api_secret, testnet=settings.testnet)
        # Set base URL explicitly for futures testnet
        self.client.FUTURES_URL = settings.base_url

    def mode(self) -> str:
        return "real"

    def place_order(self, req: OrderRequest) -> OrderResponse:
        req.validate()
        side = SIDE_BUY if req.side == "BUY" else SIDE_SELL
        try:
            if req.type == "MARKET":
                resp = self.client.futures_create_order(
                    symbol=req.symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=req.quantity,
                    newClientOrderId=req.clientOrderId
                )
            elif req.type == "LIMIT":
                resp = self.client.futures_create_order(
                    symbol=req.symbol,
                    side=side,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    price=str(req.price),
                    quantity=req.quantity,
                    newClientOrderId=req.clientOrderId
                )
            elif req.type == "STOP_LIMIT":
                resp = self.client.futures_create_order(
                    symbol=req.symbol,
                    side=side,
                    type=ORDER_TYPE_STOP_LOSS_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    price=str(req.price),
                    stopPrice=str(req.stopPrice),
                    quantity=req.quantity,
                    newClientOrderId=req.clientOrderId
                )
            else:
                raise ValueError("Unsupported order type")

            # Normalize response
            status = resp.get("status", "NEW")
            executed = float(resp.get("executedQty", 0.0))
            price = float(resp.get("price", 0.0)) if resp.get("price") else None
            order_id = str(resp.get("orderId", gen_order_id()))
            return OrderResponse(
                symbol=req.symbol,
                side=req.side,
                type=req.type,
                status=status,
                orderId=order_id,
                transactTime=resp.get("updateTime") or resp.get("transactTime") or now_ms(),
                price=price,
                origQty=float(resp.get("origQty", req.quantity)),
                executedQty=executed,
                clientOrderId=resp.get("clientOrderId"),
                extra={"raw": resp}
            )
        except (BinanceAPIException, BinanceRequestException) as e:
            self.log.error(f"Binance error: {e}")
            raise
