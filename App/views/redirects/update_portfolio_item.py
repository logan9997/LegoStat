from django.shortcuts import redirect

def update_portfolio_item(request, item_id:str):

    return redirect('portfolio_item', item_id) 