from django.shortcuts import render

def buy(request):

    context = {}

    return render(request, 'App/buy.html', context=context)