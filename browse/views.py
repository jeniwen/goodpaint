from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def info(request):
    context = {}
    context['username'] = request.user.username
    return render(request, 'browse/base.html', context)
