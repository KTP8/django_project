from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from .forms import ReservationForm

# Existing F-1 Views
def index(request):
    return render(request, 'hello_world/index.html')

def booking(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'hello_world/booking_confirm.html')
    else:
        form = ReservationForm()
    return render(request, 'hello_world/booking.html', {'form': form})

# New F-2: Reservation CRUD Views

def reservation_list(request):
    """Owner's dashboard showing all reservations."""
    reservations = Reservation.objects.all().order_by('-date', '-time')
    return render(request, 'hello_world/reservation_list.html', {'reservations': reservations})

def reservation_detail(request, pk):
    """Detail view for a single reservation."""
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'hello_world/reservation_detail.html', {'reservation': reservation})

def reservation_delete(request, pk):
    """Delete a reservation after confirmation."""
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation_list')
    return render(request, 'hello_world/reservation_delete_confirm.html', {'reservation': reservation})
