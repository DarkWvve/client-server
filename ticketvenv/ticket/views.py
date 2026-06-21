import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Ticket
from .form import CreateTicketForm, UpdateTicketForm
from . import emails
from users.models import User
from django.contrib.auth.decorators import login_required

import openpyxl


@login_required(login_url='login')
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    t = User.objects.get(username=ticket.created_by.username)
    tickets_per_user = t.created_by.all()
    context = {
        'ticket': ticket,
        'tickets_per_user': tickets_per_user
    }
    return render(request, 'ticket/ticket_details.html', context)


# create ticket
@login_required(login_url='login')
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.save()
            emails.notify_ticket_created(var)
            messages.success(request, 'Your ticket has been successfully submitted. An engineer would be assigned soon.')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check your credentials')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {
            'form': form
        }
        return render(request, 'ticket/create_ticket.html', context)
    

@login_required(login_url='login')
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.is_resolved:
        if request.method == 'POST':
            form = CreateTicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your ticket has been updated and all the changes are saved in the database.')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong. Please check your credentials')
                # return redirect('update-ticket', pk=pk)
        else:
            form = UpdateTicketForm(instance=ticket)
            context = {
                'form': form
            }
            return render(request, 'ticket/update_ticket.html', context)
    else:
        messages.warning(request, 'You cannot update a resolved ticket.')
        return redirect('dashboard')

@login_required(login_url='login')
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    context = {
        'tickets': tickets
    }
    return render(request, 'ticket/all_tickets.html', context)

# view ticket queue
@login_required(login_url='login')
def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status='Pending')
    context = {
        'tickets': tickets
    }
    return render(request, 'ticket/ticket_queue.html', context)

# accept a ticket from the queue
@login_required(login_url='login')
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    emails.notify_status_changed(ticket)
    messages.info(request, 'Ticket has been accepted. Please resolve as soon as possible!')
    return redirect('workspace')

# close a ticket
@login_required(login_url='login')
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.closed_date = datetime.datetime.now()
    ticket.save()
    emails.notify_status_changed(ticket)
    messages.info(request, 'Ticket has been Resolved. Thank you brilliant support engineer!')
    return redirect('ticket-queue')

# ticket engineer is working on
@login_required(login_url='login')
def workspace(request):
    ticket = Ticket.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {
        'ticket': ticket
    }
    return render(request, 'ticket/workspace.html', context)

# all closed/resolved tickets
@login_required(login_url='login')
def all_tickets_resolved(request):
    ticket = Ticket.objects.filter(assigned_to=request.user, is_resolved=True)
    context = {
        'ticket': ticket
    }
    return render(request, 'ticket/all_tickets_resolved.html', context)


# export user's tickets to excel
@login_required(login_url='login')
def export_tickets_excel(request):
    tickets = Ticket.objects.filter(created_by=request.user)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Tickets'

    headers = ['Ticket Number', 'Title', 'Description', 'Status', 'Assigned To', 'Created']
    ws.append(headers)

    for t in tickets:
        ws.append([
            str(t.ticket_number),
            t.title,
            t.description,
            t.ticket_status,
            t.assigned_to.username if t.assigned_to else 'Not Assigned',
            t.date_created.strftime('%Y-%m-%d %H:%M'),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=tickets.xlsx'
    wb.save(response)
    return response
