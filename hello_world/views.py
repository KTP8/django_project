from django.shortcuts import render

def index(request):
    """
    Renders the home page (index.html) for the restaurant booking system.
    """
    return render(request, 'hello_world/index.html')

def booking(request):
    """
    Renders the booking page (booking.html) for the restaurant booking system.
    """
    return render(request, 'hello_world/booking.html')
