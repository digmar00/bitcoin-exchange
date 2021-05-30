import requests


class BitcoinInfo:

    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        self.orders = []

        self.params = {
            'convert': 'USD'
        }

        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'e8698b4f-51fb-4668-aff9-a7e608d01a34'
        }

    def get_price(self, convert='USD'):
        self.params["convert"] = str(convert)
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()

        return r["data"][0]["quote"][convert]["price"]



