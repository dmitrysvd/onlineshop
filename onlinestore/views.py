from django.shortcuts import render


def index(request):
    return render(request, 'onlinestore/index.html')
