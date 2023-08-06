from django.shortcuts import render

def item(request):

    context = {}

    return render(request, 'App/item.html', context=context)