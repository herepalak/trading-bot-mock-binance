import os

def get_env_flag(name: str, default: bool=False) -> bool:
    v = os.getenv(name, "").lower()
    if v in ("1","true","yes","on"):
        return True
    if v in ("0","false","no","off"):
        return False
    return default

class Settings:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY", "")
        self.api_secret = os.getenv("BINANCE_API_SECRET", "")
        self.testnet = get_env_flag("BINANCE_TESTNET", True)
        self.base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

    def has_keys(self) -> bool:
        return bool(self.api_key and self.api_secret)
