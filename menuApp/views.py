from django.shortcuts import render


def index(request, name):
    return render(request, 'menu.html', {'name': name})

