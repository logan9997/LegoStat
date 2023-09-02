from django.shortcuts import redirect

def logout(request):
    request.session['user_id'] = -1
    return redirect('home')