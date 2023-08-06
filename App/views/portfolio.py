from django.shortcuts import render

def portfolio(request):

    context = {}

    return render(request, 'App/portfolio.html', context=context)