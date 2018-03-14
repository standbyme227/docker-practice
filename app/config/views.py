from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()

def index(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'index.html', context)