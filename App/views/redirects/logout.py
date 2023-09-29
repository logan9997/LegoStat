from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest


def logout(request:WSGIRequest):
    request.session['user_id'] = -1
    return redirect('home')