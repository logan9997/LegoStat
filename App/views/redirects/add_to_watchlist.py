from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from ...models import Watchlist

def add_to_watchlist(request:WSGIRequest, item_id:str):
    user_id = request.session.get('user_id', -1)
    if user_id != -1:
        new_entry = Watchlist(user_id=user_id, item_id=item_id)
        new_entry.save()
    return redirect('item', item_id)