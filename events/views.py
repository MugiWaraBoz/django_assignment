from datetime import date
from django.shortcuts import render, redirect
from events.models import Participant,Event,Category
from events.forms import EventModelForm
from django.db.models import Count, Q

# Create your views here.
def dashboard(request):
    events = Event.objects.all().select_related('category').prefetch_related('participants')
    categories = Category.objects.all()
    current_date = date.today()

    count = events.aggregate(        
        total_events = Count('id', distinct=True),
        Today_events = Count('id',filter=Q(date=current_date)),
        upcoming_events = Count('id', filter=Q(date__gt=current_date), distinct=True),
        past_events = Count('id', filter=Q(date__lt=current_date), distinct=True),
        participants_cnt = Count('participants__id'),
    )

    context = {
        "Events" : events,
        "categories": categories,
        "count": count,

    }
    return render(request, 'dashboard.html', context)

def event_details(request, event_id):
    event = Event.objects.prefetch_related('participants').get(id=event_id)

    context = {
        "event": event,
        "count": event.participants.aggregate(participants_cnt=Count('id')),
    }

    return render(request, "event-details.html", context)


def event_form(request):
    form = EventModelForm()

    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        "form": form,
        "title": "Add a New Event",
    }

    return render(request, "event-form.html", context)

def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    form = EventModelForm(instance=event)

    if request.method == "POST":
        form = EventModelForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        "form": form,
        "title": "Edit Event",
    }

    return render(request, "event-form.html", context)



def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event.delete()
    except Event.DoesNotExist:
        pass  # Optionally handle the case where the event does not exist

    return redirect('dashboard')