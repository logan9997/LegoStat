from responses import Response
from db import DB
from pprint import pprint

class Update:

    def __init__(self) -> None:
        self.db = DB()
        self.response = Response()

    def get_price_data(self, item_id:str, condition:str) -> dict:
        data = self.response.get_response(
            f'items/MINIFIG/{item_id}/price?new_or_used={condition}'
        )
        return data
    
    def insert_price_info(self, info):
        self.db.insert_price_info(info)

    def parse_ids(self):
        self.ids = self.db.get_ids()
        for item_id in self.ids:
            for condition in ['N', 'U']:
                data = self.get_price_data(item_id, condition)
                self.insert_price_info(data)


update = Update()
update.parse_ids()