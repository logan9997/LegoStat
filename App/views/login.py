from django.shortcuts import render, redirect
from ..forms import Login
from ..models import User

def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            user = User.objects.filter(**form.cleaned_data)
            if len(user) == 1:
                request.session['user_id'] = user.values_list(
                    'user_id', flat=True
                )[0]
                return redirect('home')
            
    context = {
        'form':Login
    }
    return render(request, 'App/login.html', context=context)