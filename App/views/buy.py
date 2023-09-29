from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

def buy(request:WSGIRequest):

    context = {}

    return render(request, 'App/buy.html', context=context)