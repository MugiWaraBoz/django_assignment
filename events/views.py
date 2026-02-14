from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from events.models import Event,Category,RSVP
from events.forms import EventModelForm


# Checks
def is_admin(u):
    return u.groups.filter(name="Admin").exists()

def is_manager(u):
    return u.groups.filter(name="Manager").exists()

def participants(u):
    return u.groups.filter(name="Participants").exists()


# Create your views here.
def dashboard(request):
    events = Event.objects.all().select_related('category').prefetch_related('participants')
    categories = Category.objects.all()
    current_date = date.today()
    category_id = request.GET.get('category')
    filter_events = request.GET.get('filter_events')
    search_query = request.GET.get('search')
    
    has_rsvp = RSVP.objects.select_related('event', 'participants').filter(participants = request.user, is_going=True)
    rsvped_event_ids = has_rsvp.values_list('event_id', flat=True)
    print(rsvped_event_ids)


    count = events.aggregate(        
        total_events = Count('id', distinct=True),
        Today_events = Count('id',filter=Q(date=current_date)),
        upcoming_events = Count('id', filter=Q(date__gt=current_date), distinct=True),
        past_events = Count('id', filter=Q(date__lt=current_date), distinct=True),
        participants_cnt = Count('participants__id', distinct=True),
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
        "rsvped_event_ids": rsvped_event_ids

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

@login_required(login_url="error-404")
@user_passes_test(lambda u: is_admin(u) or is_manager(u), login_url="home")
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

@login_required(login_url="error-404")
@user_passes_test(lambda u: is_admin(u) or is_manager(u), login_url="home")
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

@login_required(login_url="error-404")
@user_passes_test(lambda u: is_admin(u) or is_manager(u), login_url="home")
def delete_event(request, event_id):
    """
    next_url places the current active url after deletion
    """
    next_url = request.GET.get('next', 'dashboard')

    try:
        event = Event.objects.get(id=event_id)
        event.delete()
        messages.success(request, "Event deleted successfully!")
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")

    # print(next_url)
    return redirect(next_url)


@login_required(login_url="error-404")
def rsvp_event(request, event_id):

    next_url = request.GET.get('next', 'dashboard')

    event = Event.objects.get(id=event_id)
    rsvp_ins = RSVP.objects.select_related('event', 'participants')

    if not rsvp_ins.filter(event__id=event_id, participants_id=request.user.id).exists():
        RSVP.objects.create(event = event, participants = request.user)
        messages.success(request, "Successfully RSVP the event")
    else :
        messages.error(request, "Already participating this event")

    return redirect(next_url)


@login_required(login_url="error-404")
def rsvp_removed(request, event_id):
    next_url = request.GET.get('next', 'dashboard')

    rsvp_ins = RSVP.objects.select_related('event', 'participants').filter(event__id=event_id, participants_id=request.user.id)
    if rsvp_ins.exists():
        rsvp_ins.delete()
        messages.success(request, "RSVP Removed") 
    else :
        messages.error(request, "Not yet RSVP")

    return redirect(next_url)