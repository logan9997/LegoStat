from django.shortcuts import render
from ..models import Item, Price, Watchlist, Portfolio
from django.db.models import Max, Exists, Count, Subquery, OuterRef, Value, Case, F, FloatField, Sum, Value, When
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.functions import Coalesce
from config import Options
from utils import get_similar_items


def item(request:WSGIRequest, item_id:str):

    user_id = request.session.get('user_id', -1)

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
        in_watchlist=Exists(Watchlist.objects.filter(
            user_id=user_id,item_id=item_id)),
        portfolio_quantity=Coalesce(
            Subquery(
                Portfolio.objects.filter(
                    user_id=user_id, item_id=OuterRef('item_id')
                ).values(c=Count('item_id'))[:1]
            ),
            Value(0)
        ),
        portfolio_value=F('portfolio_quantity') * (
            Case(
                When(price__condition='N', then=F('price_new')),
                default=Value(0),
                output_field=FloatField()
            ) +
            Case(
                When(price__condition='U', then=F('price_used')),
                default=Value(0),
                output_field=FloatField()
            )
        )
    )[0]

    item_info['graph_prices_new'] = list(Price.objects.filter(item_id=item_id, condition='N').values_list('avg_price', flat=True))
    item_info['graph_prices_used'] = list(Price.objects.filter(item_id=item_id, condition='U').values_list('avg_price', flat=True))

    item_info['graph_quantities_new'] = list(Price.objects.filter(item_id=item_id, condition='N').values_list('total_quantity', flat=True))
    item_info['graph_quantities_used'] = list(Price.objects.filter(item_id=item_id, condition='U').values_list('total_quantity', flat=True))

    item_info['graph_dates'] = list(Price.objects.filter(item_id=item_id, condition='N').values_list('date', flat=True))

    similar_items = get_similar_items(
        item_info['item_name'], item_info['item_type']
    )
    similar_items = Item.objects.filter(
        item_id__in=similar_items
    ).values('item_id', 'item_name')
    

    context = {
        'item_info':item_info,
        'graph_metrics':Options.GRAPH_METRICS,
        'similar_items':similar_items
    }

    return render(request, 'App/item.html', context=context)



