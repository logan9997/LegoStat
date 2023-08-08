from django.shortcuts import render
from ..models import Item, Price
from config import Date
from datetime import datetime as dt

def item(request, item_id:str):

    price_table_filters = {'item_id':item_id, 'date':dt.today().strftime(Date.DATE_FORMAT)}

    item_info = Item.objects.filter(item_id=item_id, price__date=dt.today(
        ).strftime(Date.DATE_FORMAT)).values(
            'item_id', 'item_name', 'year_released', 'item_type', 'views',
            'price__date', 'price__avg_price', 'price__total_quantity',
            'price__condition'
        ).annotate(
        price_new=Price.objects.filter(**price_table_filters, condition='N'
            ).values_list('avg_price', flat=True),    
        price_used=Price.objects.filter(**price_table_filters, condition='U'
            ).values_list('avg_price', flat=True),
        quantity_new=Price.objects.filter(**price_table_filters, condition='N'
            ).values_list('total_quantity', flat=True),
        quantity_used=Price.objects.filter(**price_table_filters, condition='U'
            ).values_list('total_quantity', flat=True),
    )[0]

    context = {
        'item_info':item_info
    }

    return render(request, 'App/item.html', context=context)