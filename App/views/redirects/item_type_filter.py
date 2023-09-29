from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest

def item_type_filter(request:WSGIRequest, redirect_view:str):
    request.session['item_type_filter'] = request.POST.get('item-type_filter', 'ALL')
    return redirect(redirect_view)