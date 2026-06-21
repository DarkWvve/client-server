from django.shortcuts import render, redirect

from ticket.models import Ticket


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
