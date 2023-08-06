from django.shortcuts import render

def watchlist(request):

    context = {}

    return render(request, 'App/watchlist.html', context=context)