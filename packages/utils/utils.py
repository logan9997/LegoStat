import time
from config import SimilarItem
from db import DB
import itertools

db = DB()

def clean_html_codes(string:str):
    codes = {
        '&#40;':'(',
        '&#41;':')',
        '&#39;': "'"
    }
    for k, v in codes.items():
        if k in string:
            string = string.replace(k, v)
    return string

def item_type_convert(item_type:str):
    if len(item_type) > 1:
        return {'MINIFIG':'M', 'SET':'S'}[item_type]
    return {'M':'MINIFIG', 'S':'SET'}[item_type]


def timer(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        finish_time = time.time() - start_time
        print(f'<{func.__name__}> Finished in {round(finish_time)} seconds.')
    return inner
    
    
def get_similar_items(item_name:str, item_type:str):
    single_words = item_name.split(' ')
    single_words = [word for word in single_words if len(word) > 2 and word not in SimilarItem.COMMON_WORDS]

    items = db.get_items_by_type(item_type, item_name, 'item_name', 'item_id')
    matches = []
    for i in range(len(single_words)):
        for item in items:
            for sub in itertools.combinations(single_words, len(single_words) - i):
                criteria = [True if s in item['item_name'] else False for s in sub]
                if all(criteria) and item['item_id'] not in matches:
                    matches.append(item['item_id'])
                    if len(matches) >= 12:
                        return matches
    return matches
