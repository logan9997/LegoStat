from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest

def pages(request:WSGIRequest, redirect_view:str):
    current_page = request.POST.get('selected_page', 1)
    request.session['current_page'] = current_page
    return redirect(redirect_view)