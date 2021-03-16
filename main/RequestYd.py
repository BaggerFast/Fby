from fby_market.settings import YaMarket
import requests
from main.models.save_dir.offer import OfferPattern
from main.models.save_dir.prices import PricePattern


class Requests:
    def __init__(self, json_name):
        self.url = f'https://api.partner.market.yandex.ru/v2/campaigns/{YaMarket.SHOP_ID}{json_name}.json'
        self.headers_str = f'OAuth oauth_token=\"{YaMarket.TOKEN}\", oauth_client_id=\"{YaMarket.CLIENT_ID}\"'
        self.headers = {'Authorization': self.headers_str, 'Content-type': 'application/json'}
        self.json_data = self.get_json()

    def get_json(self, ):
        data = requests.get(self.url, headers=self.headers)
        json_data = data.json()
        print(json_data)
        if "OK" in json_data['status']:
            json_data = self.check_next_page(json_data=json_data)
        return json_data

    def check_next_page(self, json_data):
        raise NotImplementedError

    def get_next_page(self, next_page_token=None):
        if next_page_token:
            self.url += f'?page_token={next_page_token}'
        data = requests.get(self.url, headers=self.headers)
        return data.json()

    def save(self):
        raise NotImplementedError


class OfferList(Requests):
    def __init__(self):
        super().__init__(json_name='/offer-mapping-entries')

    def check_next_page(self, json_data):
        while 'nextPageToken' in json_data['result']['paging']:  # если страница не последняя, читаем следующую
            next_page_token = json_data['result']['paging']['nextPageToken']
            next_json_object = self.get_next_page(next_page_token)
            json_data['result']['offerMappingEntries'] += next_json_object['result']['offerMappingEntries']
            json_data['result']['paging'] = next_json_object['result']['paging']
        return json_data

    def save(self):
        OfferPattern(json=self.json_data['result']['offerMappingEntries']).save()


class OfferPrice(Requests):
    def __init__(self):
        super().__init__(json_name='/offer-prices')

    def check_next_page(self, json_data):
        while 'nextPageToken' in json_data['result']['paging']:  # если страница не последняя, читаем следующую
            next_page_token = json_data['result']['paging']['nextPageToken']
            next_json_object = self.get_next_page(next_page_token)
            json_data['result']['offers'] += next_json_object['result']['offers']
            json_data['result']['paging'] = next_json_object['result']['paging']
        return json_data

    def save(self):
        PricePattern(json=self.json_data['result']['offers']).save()
