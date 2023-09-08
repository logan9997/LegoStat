from django.shortcuts import redirect

def graph_range(request, redirect_view):
    request.session['graph_range'] = request.POST.get('graph_range', 'MAX')
    return redirect(redirect_view)