from django.shortcuts import render

def trending(request):

    context = {}

    return render(request, 'App/trending.html', context=context)