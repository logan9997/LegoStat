from django.shortcuts import redirect

def item_type_filter(request, redirect_view:str):
    request.session['item_type_filter'] = request.POST.get('item-type_filter', 'ALL')
    return redirect(redirect_view)