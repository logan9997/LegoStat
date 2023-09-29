from django.shortcuts import render
from ..models import Price, Item, Portfolio

def portfolio_item(request, item_id:str):

    user_id = request.session.get('user_id', -1)

    item_info = Item.objects.filter(item_id=item_id).values()[0]
    
    item_prices = Price.objects.filter(item_id=item_id)
    latest_entry_N = item_prices.filter(condition='N').latest('date')
    latest_entry_U = item_prices.filter(condition='U').latest('date')

    portfolio_items = Portfolio.objects.filter(item_id=item_id, user_id=user_id)
    quantity_owned_N = portfolio_items.filter(condition='N').count()
    quantity_owned_U = portfolio_items.filter(condition='U').count()

    item_info.update({
        'avg_price_new': latest_entry_N.avg_price,
        'avg_price_used': latest_entry_U.avg_price,
        'total_quantity_new': latest_entry_N.total_quantity,
        'total_quantity_used': latest_entry_U.total_quantity,
        'quantity_owned_new':quantity_owned_N,
        'quantity_owned_used':quantity_owned_U
    })

    context = {
        'item_info':item_info,
        'items':portfolio_items.values()
    }

    return render(request, 'App/portfolio_item.html', context=context) 