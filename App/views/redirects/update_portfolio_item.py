from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest

from ...forms import UpdatePortfolioIten
from ...models import Portfolio

def update_portfolio_item(request:WSGIRequest, entry_id:int, item_id:str):

    if request.method == 'POST':
        form = UpdatePortfolioIten(request.POST)
        if form.is_valid():
            portfolio_item = Portfolio.objects.filter(entry_id=entry_id)
            portfolio_item.update(**form.cleaned_data)

    return redirect('portfolio_item', item_id) 