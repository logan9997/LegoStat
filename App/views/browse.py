from django.shortcuts import render

def browse(request):

    context = {}

    return render(request, 'App/browse.html', context=context)