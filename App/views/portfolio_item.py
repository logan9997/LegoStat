from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

from ..models import Price, Item, Portfolio
from config import ModelValidations as MV, Options
from utils import GraphData

def portfolio_item(request:WSGIRequest, item_id: str):

    user_id = request.session.get('user_id', -1)

    item_info = Item.objects.filter(item_id=item_id).values()[0]

    item_prices = Price.objects.filter(item_id=item_id)
    latest_entry_new = item_prices.filter(condition='N').latest('date')
    latest_entry_used = item_prices.filter(condition='U').latest('date')

    portfolio_items = Portfolio.objects.filter(item_id=item_id, user_id=user_id)
    quantity_owned_new = portfolio_items.filter(condition='N').count()
    quantity_owned_used = portfolio_items.filter(condition='U').count()

    item_info.update({
        'avg_price_new': latest_entry_new.avg_price,
        'avg_price_used': latest_entry_used.avg_price,
        'total_quantity_new': latest_entry_new.total_quantity,
        'total_quantity_used': latest_entry_used.total_quantity,
        'quantity_owned_new': quantity_owned_new,
        'quantity_owned_used': quantity_owned_used
    })

    graph_data = GraphData(Price, item_info['item_id'])
    item_info.update(graph_data.get_metrics())
    item_info.update({'graph_dates':graph_data.get_dates()})

    context = {
        'item_info': item_info,
        'items': portfolio_items.values(),
        'notes_max_length': MV.Lengths.NOTES,
        'graph_metrics':Options.GRAPH_METRICS
    }

    return render(request, 'App/portfolio_item.html', context=context)
