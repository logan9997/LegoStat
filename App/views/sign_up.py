from django.shortcuts import render, redirect
from ..forms import SignUp
from ..models import User

def sign_up(request):

    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            new_user = User(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            new_user.save()
            request.session['user_id'] = new_user.pk
            return redirect('home')
            
    context = {
        'form':SignUp
    }

    return render(request, 'App/sign_up.html', context=context)