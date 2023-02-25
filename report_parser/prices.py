import os
import sys
import requests
from requests import Session
import json
from typing import List, Dict, Optional

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot", "config")))

from config.bird_config import CmcConfig


class Prices:
    def __init__(self, sts_secrets: Optional[Dict[str, str]] = None):
        self.coins_available = self.initialize_id_name_mapping()
        self.cmc_config = CmcConfig(sts_secrets)
        self.cmc_key = self.cmc_config.cmc_key

    def initialize_id_name_mapping(self):
        with open("assets/coin_list.json", "r") as f:
            mapping = json.load(f)
        return mapping

    def get_prices(self, tokens_represented: List[str]) -> Dict[str, Dict[str, float]]:
        token_symbols = ",".join(tokens_represented)

        url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
        parameters = {"symbol": token_symbols}
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.cmc_key,
        }
        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        response = json.loads(response.text)
        
        prices = {"24hr": {}, "7d": {}, "30d": {}}
        for token_symbol, r in response["data"].items():
            r = sorted(r, key=lambda d: d['cmc_rank'] if d['cmc_rank'] is not None else 10000000.0, reverse=True)
            r = r[0] # highest ranking entry

            daily=r["quote"]["USD"]["percent_change_24h"]
            weekly = r["quote"]["USD"]["percent_change_7d"]
            monthly = r["quote"]["USD"]["percent_change_30d"]

            daily = round(daily, 2) if daily else None
            weekly = round(weekly, 2) if weekly else None
            monthly = round(monthly, 2) if monthly else None

            prices["24hr"][token_symbol] = daily
            prices["7d"][token_symbol] = weekly
            prices["30d"][token_symbol] = monthly
        return prices

if __name__ == "__main__":
    c = Prices()
    data = c.get_prices(tokens_represented=["btc", "lrc", "rose", "sol"])
    print(data)