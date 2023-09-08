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
        result = func(*args, **kwargs)
        finish_time = time.time() - start_time
        print(f'<{func.__name__}> Finished in {round(finish_time, 6)} seconds.')
        return result
    return inner
    
@timer
def get_similar_items(item_name:str, item_type:str):
    item_name_words = item_name.split(' ')
    item_name_words = [
        word for word in item_name_words 
        if len(word) > 2 and 
        word not in SimilarItem.COMMON_WORDS
    ]

    items = db.get_items_by_type(item_type, item_name, select_fields=('item_name', 'item_id'))

    len_item_name_words = len(item_name_words)
    
    shorten_max_combinations = {
        len_item_name_words >= 14 : 6,
        len_item_name_words < 14 and len_item_name_words >= 8: 5,
        len_item_name_words < 8 and len_item_name_words >= 6: 4,
        len_item_name_words < 6: len_item_name_words 
    }
    num_combinations = shorten_max_combinations[True]

    matches = []
    for i in range(len(item_name_words)):
        for item in items:
            for sub in itertools.combinations(item_name_words, num_combinations - i):
                if item['item_id'] in matches:
                    continue

                all_substrings_present = True
                for s in sub:
                    if s not in item['item_name']:
                        all_substrings_present = False
                        break

                if all_substrings_present:
                    matches.append(item['item_id'])
                    if len(matches) >= SimilarItem.MAX_MATHCES:
                        return matches
                    break
    return matches
