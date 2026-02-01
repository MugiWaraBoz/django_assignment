from django.shortcuts import render, redirect
from events.models import Participant,Event,Category
from events.forms import EventModelForm

# Create your views here.
def dashboard(request):
    events = Event.objects.all();
    
    context = {
        "Events" : events,
        "categories": Category.objects.all(),
    }
    return render(request, 'dashboard.html', context)

def event_details(request, event_id):
    event = Event.objects.get(id=event_id)

    context = {
        "event": event
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