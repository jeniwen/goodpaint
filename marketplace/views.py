from django.shortcuts import redirect
def default(request):
    return redirect('/account/login')