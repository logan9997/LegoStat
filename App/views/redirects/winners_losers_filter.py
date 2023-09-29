from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest


def winners_losers_filter(request:WSGIRequest, redirect_view:str):
    request.session['winners_losers_filter'] = request.POST.get('winners_losers_filter')
    return redirect(redirect_view)