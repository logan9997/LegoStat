from django.shortcuts import render
from ..models import Portfolio, Price
from django.db.models import F, Count, Sum, OuterRef
from django.core.handlers.wsgi import WSGIRequest
from utils import GraphData


def portfolio(request: WSGIRequest):

    user_id = request.session.get('user_id', -1)

    portfolio_items = Portfolio.objects.filter(
        user_id=user_id
    ).values(
        'condition',
        'item_id',
        item_name=F('item__item_name'),
    ).annotate(
        quantity=Count('item_id'),
        total_value=Price.objects.filter(
            item_id=OuterRef('item_id'),
            condition=OuterRef('condition'),
            date='2023-09-09'
        ).values_list('avg_price', flat=True)
    ).order_by('item_id')

    for item in portfolio_items:

        item['avg_price_new'] = Price.objects.filter(
            item_id=item['item_id'], condition='N'
        ).latest('date').avg_price

        item['avg_price_used'] = Price.objects.filter(
            item_id=item['item_id'], condition='U'
        ).latest('date').avg_price

        item['total_quantity_new'] = Price.objects.filter(
            item_id=item['item_id'], condition='N'
        ).latest('date').total_quantity

        item['total_quantity_used'] = Price.objects.filter(
            item_id=item['item_id'], condition='U'
        ).latest('date').total_quantity

        graph_data = GraphData(Price, item['item_id'])
        item.update(graph_data.get_metrics())
        item['graph_dates'] = graph_data.get_dates()

    context = {
        'portfolio_items': list(portfolio_items)
    }

    return render(request, 'App/portfolio.html', context=context)
