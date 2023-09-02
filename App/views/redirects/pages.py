from django.shortcuts import redirect

def pages(request, redirect_view:str):
    current_page = request.POST.get('selected_page', 1)
    request.session['current_page'] = current_page
    return redirect(redirect_view)