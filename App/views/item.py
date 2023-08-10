from django.shortcuts import render
from ..models import Item, Price
from django.db.models import Max

def item(request, item_id:str):

    max_date = Price.objects.filter(item_id=item_id).aggregate(max_date=Max('date')).get('max_date')
    price_table_filters = {'item_id':item_id, 'date':max_date}

    item_info = Item.objects.filter(item_id=item_id, price__date=max_date).values(
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