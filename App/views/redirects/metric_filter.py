from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest

def metric_filter(request:WSGIRequest, redirect_view:str):
    request.session['metric_filter'] = request.POST.get('metric_filter')
    return redirect(redirect_view)