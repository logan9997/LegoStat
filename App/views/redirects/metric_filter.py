from django.shortcuts import redirect

def metric_filter(request, redirect_view:str):
    request.session['metric_filter'] = request.POST.get('metric_filter')
    return redirect(redirect_view)