from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from WhatsUp.models import Ticket
from WhatsUp.forms import LoginForm, AddTicket
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    html = "index.html"

    tickets = Ticket.objects.all()
    new = tickets.filter(ticket_status='N').order_by("-post_date")
    in_progress = tickets.filter(ticket_status='IP').order_by("-post_date")
    done = tickets.filter(ticket_status='D').order_by("-post_date")
    invalid = tickets.filter(ticket_status='IV').order_by("-post_date")

    return render(request, html, {'new': new, 'in_progress': in_progress, 'done': done, 'invalid': invalid})

@login_required
def addticketview(request):
    html = 'generic_form.html'

    if request.method == "POST":
        form = AddTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                title=data['title'],
                description=data['description'],
                ticket_status=data['ticket_status'],
                created_by=request.user,
                assigned_user=data['assigned_user']
            )
        return HttpResponseRedirect(reverse('homepage'))
    form = AddTicket()
    return render(request, html, {'form': form})

@login_required
def editticketview(request, id):
    html = "generic_form.html"
    instance = Ticket.objects.get(id=id)
    if request.method == "POST":
        form = AddTicket(request.POST, instance=instance)
        form.save()


        if instance.ticket_status == "D":
            instance.finished_user = instance.assigned_user
            instance.assigned_user = None
            form.save()
        elif instance.ticket_status == "IP" and instance.assigned_user is None:
            instance.assigned_user = instance.created_by
        elif instance.ticket_status == "IV":
            instance.finished_user = None
            instance.assigned_user = None
            form.save()
        elif instance.assigned_user is not None:
            instance.ticket_status = "IP"
            form.save()

        return HttpResponseRedirect(reverse('homepage'))

    form = AddTicket(instance=instance)

    return render(request, html, {'form': form})


def userpageview(request, id):
    user_html = 'user_page.html'

    created = Ticket.objects.filter(created_by=id)
    assigned = Ticket.objects.filter(assigned_user=id)
    finished = Ticket.objects.filter(finished_user=id)

    return render(request, user_html,
                  {'created': created,
                   'assigned': assigned,
                   'finished': finished})


def ticketview(request, id):
    html = 'ticket.html'
    ticket = Ticket.objects.filter(id=id)

    return render(request, html, {'ticket': ticket})


def login_view(request):
    html = 'generic_form.html'

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
        if user:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))

    form = LoginForm()

    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))