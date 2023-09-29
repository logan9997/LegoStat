from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest


def watchlist(request:WSGIRequest):

    context = {}

    return render(request, 'App/watchlist.html', context=context)