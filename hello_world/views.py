from django.shortcuts import render


def index(request):
    print("DEBUG: inside index view!")
    return render(request, 'hello_world/index.html')


def booking(request):
    return render(request, 'hello_world/booking.html')
