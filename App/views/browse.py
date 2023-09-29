from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

def browse(request:WSGIRequest):

    context = {}

    return render(request, 'App/browse.html', context=context)