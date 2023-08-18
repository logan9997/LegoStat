from responses import Response
from db import DB
from utils import item_type_convert, timer

class Update:

    def __init__(self) -> None:
        self.db = DB()
        self.response = Response()

    def get_price_data(self, item_id:str, condition:str, item_type:str) -> dict:
        data = self.response.get_response(
            f'items/{item_type}/{item_id}/price?new_or_used={condition}'
        )
        return data
    
    def insert_price_info(self, info):
        self.db.insert_price_info(info)

    def parse_ids(self):
        self.ids = self.db.get_ids()
        for item_id in self.ids:
            item_type = self.db.get_item_type(item_id)
            item_type = item_type_convert(item_type)
            for condition in ['N', 'U']:
                data = self.get_price_data(item_id, condition, item_type)
                self.insert_price_info(data)

@timer
def main():
    update = Update()
    update.parse_ids()


if __name__ == '__main__':
    main()