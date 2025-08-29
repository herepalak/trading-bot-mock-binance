import argparse, json, sys
from .config import Settings
from .logger import setup_logger
from .orders import OrderRequest
from .client import choose_client

def build_parser():
    p = argparse.ArgumentParser(description="Simplified Trading Bot (Binance Futures Testnet)")
    sub = p.add_subparsers(dest="command", required=True)

    place = sub.add_parser("place", help="Place an order")
    place.add_argument("--symbol", required=True, help="e.g., BTCUSDT")
    place.add_argument("--side", required=True, choices=["BUY","SELL"])
    place.add_argument("--type", required=True, choices=["MARKET","LIMIT","STOP_LIMIT"])
    place.add_argument("--qty", required=True, type=float, help="Order quantity")
    place.add_argument("--price", type=float, help="Limit/Stop-Limit price")
    place.add_argument("--stopPrice", type=float, help="Stop-Limit stop price")
    place.add_argument("--clientOrderId", type=str, help="Optional client order id")
    place.add_argument("--mode", choices=["auto","mock","real"], default="auto", help="Execution mode")

    return p

def main(argv=None):
    argv = argv or sys.argv[1:]
    logger = setup_logger()
    parser = build_parser()
    args = parser.parse_args(argv)

    settings = Settings()
    client = choose_client(args.mode, settings)
    logger.info(f"Using client mode: {client.mode()}")

    if args.command == "place":
        req = OrderRequest(
            symbol=args.symbol.upper(),
            side=args.side,
            type=args.type,
            quantity=args.qty,
            price=args.price,
            stopPrice=args.stopPrice,
            clientOrderId=args.clientOrderId
        )
        try:
            logger.info(f"Placing order: {req}")
            resp = client.place_order(req)
            print(json.dumps(resp.to_dict(), indent=2))
        except Exception as e:
            logger.exception("Order failed")
            print(json.dumps({"error": str(e)}, indent=2))
            sys.exit(1)

if __name__ == "__main__":
    main()
