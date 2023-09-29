from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest


def settings(request:WSGIRequest):

    context = {}

    return render(request, 'App/settings.html', context=context)