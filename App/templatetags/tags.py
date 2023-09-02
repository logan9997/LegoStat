from django import template
from ..models import Item
from utils import clean_html_codes

register = template.Library()

@register.simple_tag
def get_all_item_ids():
    return list(Item.objects.all().values_list('item_id', flat=True).order_by('item_id'))

@register.simple_tag
def get_all_item_names():
    names = list(Item.objects.all().values_list('item_name', flat=True).order_by('item_id'))
    names = list(map(clean_html_codes, names))
    return names

@register.filter
def get(_dict, key):
    return _dict.get(key)

@register.filter
def add(num1, num2):
    return num1 + num2

@register.filter
def index(iterable, index:int):
    return iterable[index]

@register.filter
def abs(number:int):
    return number.__abs__()
