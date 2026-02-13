from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib import messages

from events.models import Participant,Event,Category
from events.forms import EventModelForm

# Create your views here.
def dashboard(request):
    events = Event.objects.all().select_related('category').prefetch_related('participants')
    categories = Category.objects.all()
    current_date = date.today()
    category_id = request.GET.get('category')
    filter_events = request.GET.get('filter_events')
    search_query = request.GET.get('search')


    count = events.aggregate(        
        total_events = Count('id', distinct=True),
        Today_events = Count('id',filter=Q(date=current_date)),
        upcoming_events = Count('id', filter=Q(date__gt=current_date), distinct=True),
        past_events = Count('id', filter=Q(date__lt=current_date), distinct=True),
        participants_cnt = Count('participants__id'),
    )

    if filter_events == "Upcoming Events":
        events = events.filter(date__gt=current_date)
    elif filter_events == "Past Events":
        events = events.filter(date__lt=current_date)
    elif filter_events == "All Events":
        events = events
    else:
        events = events.filter(date=current_date)

    if category_id:
        events = events.filter(category__id=category_id)

    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    context = {
        "Events" : events,
        "categories": categories,
        "count": count,
        "filter_events": filter_events,
        "search_query": search_query,

    }

    if not events.exists():
        messages.info(request, "No events found matching your criteria.")
    
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
        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Something went wrong.")
            

    context = {
        "form": form,
        "title": "Add a New Event",
    }

    return render(request, "event-form.html", context)

def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    form = EventModelForm(instance=event)

    if request.method == "POST":
        form = EventModelForm(request.POST,request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Something went wrong.")

    context = {
        "form": form,
        "title": "Edit Event",
    }
    return render(request, "event-form.html", context)



def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event.delete()
        messages.success(request, "Event deleted successfully!")
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")

    return redirect('dashboard')