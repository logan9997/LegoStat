import time
from config import SimilarItem, Pages
from db import DB
import itertools
from datetime import date, timedelta

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
def get_similar_items(item_name:str, item_type:str, item_id:str):
    item_name_words = item_name.split(' ')
    item_name_words = [
        word for word in item_name_words 
        if len(word) > 2 and 
        word not in SimilarItem.COMMON_WORDS
    ]

    items = db.get_items_by_type(item_type, item_id, select_fields=('item_name', 'item_id'))

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

class GraphData:

    def __init__(self, model, item_id, **kwargs) -> None:
        self.model = model
        self.item_id = item_id
        self.date_range = kwargs.get('date_range', 99999)
        self.today = date.today()

        self.constant_filters = {
            'date__range': [self.today - timedelta(self.date_range), self.today],
            'item_id':self.item_id
        }

    def get_metrics(self):
        graph_prices_new = list(self.model.objects.filter(
            condition='N', **self.constant_filters
        ).values_list('avg_price', flat=True).order_by('date'))
        
        graph_prices_used = list(self.model.objects.filter(
            condition='U', **self.constant_filters
        ).values_list('avg_price', flat=True).order_by('date'))

        graph_quantities_new = list(self.model.objects.filter(
            condition='N', **self.constant_filters
        ).values_list('total_quantity', flat=True).order_by('date'))

        graph_quantities_used = list(self.model.objects.filter(
            condition='U', **self.constant_filters
        ).values_list('total_quantity', flat=True).order_by('date'))

        return {
            'graph_avg_price_new': graph_prices_new,
            'graph_avg_price_used': graph_prices_used,
            'graph_total_quantity_new': graph_quantities_new,
            'graph_total_quantity_used':graph_quantities_used
        }


    def get_dates(self):
        return list(self.model.objects.filter(
                **self.constant_filters
            ).distinct('date').values_list('date', flat=True).order_by('date')
        )


def condence_pages(pages:list[int], current_page:int) -> list[int]:
    new_pages = []
    len_pages = len(pages)

    c = 0
    while True:

        c += 1
        
        if current_page + c < len_pages:
            new_pages.append(current_page + c)
        if current_page - c > 0:
            new_pages.insert(0, current_page - c + 1)

        if len(new_pages) > Pages.MAX_PAGES - 2 or c >= len_pages // 2:
            break


    new_pages.insert(0, 1)
    if len_pages not in new_pages:
        new_pages.append(len_pages)
    return new_pages

def validate_page(pages:list[int], current_page:int) -> int:
    if current_page >= pages[-1]:
        return 1
    return current_page
