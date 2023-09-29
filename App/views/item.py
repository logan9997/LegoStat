from django.shortcuts import render
from ..models import Item, Price, Watchlist, Portfolio
from django.db.models import (
    Max, Exists, Count, Subquery, OuterRef, Value,
    Case, F, FloatField, Value, When
)
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.functions import Coalesce
from config import Options
from utils import get_similar_items, GraphData


def portfolio_quantity_query(user_id) -> Coalesce:
    result = Coalesce(
        Subquery(
            Portfolio.objects.filter(
                user_id=user_id, item_id=OuterRef('item_id')
            ).values(c=Count('item_id'))[:1]
        ),
        Value(0)
    )
    return result


def portfolio_value_query() -> F:
    result = F('portfolio_quantity') * (
        Case(
            When(price__condition='N', then=F('avg_price_new')),
            default=Value(0),
            output_field=FloatField()
        ) +
        Case(
            When(price__condition='U', then=F('avg_price_used')),
            default=Value(0),
            output_field=FloatField()
        )
    )
    return result


def item(request: WSGIRequest, item_id: str):

    user_id = request.session.get('user_id', -1)

    max_date = Price.objects.filter(
        item_id=item_id
    ).aggregate(max_date=Max('date')).get('max_date')

    price_table_filters = {'item_id': item_id, 'date': max_date}
    
    item_info = Item.objects.filter(item_id=item_id, price__date=max_date).values(
        'item_id', 'item_name', 'year_released', 'item_type', 'views',
        'price__date', 'price__avg_price', 'price__total_quantity',
        'price__condition'
    ).annotate(
        avg_price_new=Price.objects.filter(
            **price_table_filters, condition='N'
        ).values_list('avg_price', flat=True),

        avg_price_used=Price.objects.filter(
            **price_table_filters, condition='U'
        ).values_list('avg_price', flat=True),

        total_quantity_new=Price.objects.filter(
            **price_table_filters, condition='N'
        ).values_list('total_quantity', flat=True),

        total_quantity_used=Price.objects.filter(
            **price_table_filters, condition='U'
        ).values_list('total_quantity', flat=True),

        in_watchlist=Exists(Watchlist.objects.filter(
            user_id=user_id, item_id=item_id)),

        portfolio_quantity=portfolio_quantity_query(user_id),
        portfolio_value=portfolio_value_query()
    )[0]

    graph_data = GraphData(Price, item_id)
    item_info.update(graph_data.get_metrics())

    dates = graph_data.get_dates()
    item_info['graph_dates'] = dates

    similar_items = get_similar_items(
        item_info['item_name'], item_info['item_type'], item_info['item_id']
    )
    similar_items = Item.objects.filter(
        item_id__in=similar_items
    ).values('item_id', 'item_name')

    context = {
        'item_info': item_info,
        'graph_metrics': Options.GRAPH_METRICS,
        'similar_items': similar_items,
        'min_date': 0,
        'max_date': (Price.objects.filter(item_id=item_id).count() // 2),
        'dates': dates
    }

    return render(request, 'App/item.html', context=context)
