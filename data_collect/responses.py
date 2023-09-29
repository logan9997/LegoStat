from requests_oauthlib import OAuth1Session
import environment_manager as EM
import json

class Response():
    def __init__(self) -> None:
        self.base_url = 'https://api.bricklink.com/api/store/v1/'
        self.keys = EM.Manager().get_items(
            'CONSUMER_KEY', 'CONSUMER_SECRET', 'TOKEN_VALUE', 'TOKEN_SECRET'
        )

        self.auth = OAuth1Session(
            self.keys['CONSUMER_KEY'], self.keys['CONSUMER_SECRET'],
            self.keys['TOKEN_VALUE'], self.keys['TOKEN_SECRET']
        )


    def get_response(self, sub_url):
        response = self.auth.get(self.base_url + sub_url)
        json_data = json.loads(response.text)

        if json_data['meta']['code'] != 200:
            print('UPDATE KEYS - https://www.bricklink.com/v2/api/register_consumer.page')
            raise Exception(str(json_data))
        return json_data['data']
