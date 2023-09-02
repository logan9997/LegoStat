from django.shortcuts import redirect

def winners_losers_filter(request, redirect_view:str):
    request.session['winners_losers_filter'] = request.POST.get('winners_losers_filter')
    return redirect(redirect_view)