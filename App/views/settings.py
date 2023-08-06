from django.shortcuts import render

def settings(request):

    context = {}

    return render(request, 'App/settings.html', context=context)