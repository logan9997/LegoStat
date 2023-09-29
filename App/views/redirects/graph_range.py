from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest


def graph_range(request:WSGIRequest, redirect_view):
    request.session['graph_range'] = request.POST.get('graph_range', 'MAX')
    return redirect(redirect_view)