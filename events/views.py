from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator

# Class Based Views Import
from django.views.generic import ListView

from events.models import Event,Category,RSVP
from events.forms import EventModelForm


# Checks
def is_admin(u):
    return u.groups.filter(name="Admin").exists()

def is_Organizer(u):
    return u.groups.filter(name="Organizer").exists()

def is_participant(u):
    return u.groups.filter(name="Participants").exists()

# Create your views here.
# def dashboard(request):
#     events = Event.objects.all().select_related('category').prefetch_related('rsvp__participants')
#     events = events.annotate(
#         going_count=Count('rsvp', filter=Q(rsvp__is_going=True))
#     )
#     categories = Category.objects.all()
#     current_date = date.today()
#     category_id = request.GET.get('category')
#     filter_events = request.GET.get('filter_events')
#     search_query = request.GET.get('search')
    
#     has_rsvp = RSVP.objects.select_related('event', 'participants')
#     if request.user.is_authenticated:
#         rsvped_event_ids = has_rsvp.filter(participants = request.user, is_going=True).values_list('event_id', flat=True)
#     # print(rsvped_event_ids)


#     count = events.aggregate(        
#         total_events = Count('id', distinct=True),
#         Today_events = Count('id',filter=Q(date=current_date)),
#         upcoming_events = Count('id', filter=Q(date__gt=current_date), distinct=True),
#         past_events = Count('id', filter=Q(date__lt=current_date), distinct=True),
#     )
    
#     # Total Participation count
    
#     participants_cnt = has_rsvp.filter(is_going=True).aggregate(total_participants=Count('participants', distinct=True))['total_participants']
#     # print(participants_cnt, "---===")

#     if filter_events == "Upcoming Events":
#         events = events.filter(date__gt=current_date)
#     elif filter_events == "Past Events":
#         events = events.filter(date__lt=current_date)
#     elif filter_events == "All Events":
#         events = events
#     else:
#         events = events.filter(date=current_date)

#     if category_id:
#         events = events.filter(category__id=category_id)

#     if search_query:
#         events = events.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

#     context = {
#         "Events" : events,
#         "categories": categories,
#         "count": count,
#         "participants_cnt" : participants_cnt,
#         "filter_events": filter_events,
#         "search_query": search_query,
#     }

#     if request.user.is_authenticated:
#         context["rsvped_event_ids"] = rsvped_event_ids
#     # print(events.values_list())

#     if not events.exists():
#         messages.info(request, "No events found matching your criteria.")
    
#     return render(request, 'dashboard.html', context)


class dashboardClassView(ListView):
    model = Event
    template_name = "dashboard.html"
    context_object_name = "Events"

    def get_base_queryset(self):
        # Count using annotate
        return Event.objects.all().select_related('category').prefetch_related(
            'rsvp__participants'
            ).annotate (
            going_count=Count('rsvp', filter=Q(rsvp__is_going=True))
        )


    def get_queryset(self):
        queryset = self.get_base_queryset()
        
        # Retrive Data for filtering
        current_date = date.today()  
        category_id = self.request.GET.get('category')
        filter_events = self.request.GET.get('filter_events')
        search_query = self.request.GET.get('search')
        
        # Filtering accordingly 
        if filter_events == "Upcoming Events":
            queryset = queryset.filter(date__gt=current_date)
        elif filter_events == "Past Events":
            queryset = queryset.filter(date__lt=current_date)
        elif filter_events == "All Events":
            queryset = queryset
        else:
            queryset = queryset.filter(date=current_date)

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        events = self.get_base_queryset()
        current_date = date.today()  
        count = events.aggregate(        
            total_events = Count('id', distinct=True),
            Today_events = Count('id',filter=Q(date=current_date)),
            upcoming_events = Count('id', filter=Q(date__gt=current_date), distinct=True),
            past_events = Count('id', filter=Q(date__lt=current_date), distinct=True),
        )
        
        rsvp = RSVP.objects.select_related('event', 'participants')
        participants_cnt = rsvp.filter(is_going=True).aggregate(total_participants=Count('participants', distinct=True))['total_participants']
        # Grabs RSVP'ed event ids to avoid RSVP'ing same event again
        if self.request.user.is_authenticated:
            rsvped_event_ids = rsvp.filter(participants = self.request.user, is_going=True).values_list('event_id', flat=True)

                                       # pythons date import

        # Counts using aggregate
    
        if self.request.user.is_authenticated:
            context["rsvped_event_ids"] = rsvped_event_ids
        
        categories = Category.objects.all()
        context["categories"] = categories
        context["count"] = count
        context["participants_cnt"] = participants_cnt
        
        if not self.get_base_queryset:
            messages.info(self.request, "No events found matching your criteria.")

        context["filter_events"] = self.request.GET.get('filter_events')
        context["search_query"] = self.request.GET.get('search')
        # context = {
        #     "Events" : events,
        #     "categories": categories,
        #     "count": count,
        #     "participants_cnt" : participants_cnt,
        #     # "filter_events": filter_events,
        #     # "search_query": search_query,
        # } 
        #   
        
        return context
    
    




def event_details(request, event_id):
    event = Event.objects.prefetch_related('rsvp__participants', 'organizers').get(id=event_id)
    context = {
        "event": event,
        "count": event.rsvp.aggregate(participants_cnt=Count('id')),
    }

    return render(request, "event-details.html", context)

@login_required(login_url="error-405")
@user_passes_test(lambda u: is_admin(u) or is_Organizer(u), login_url="home")
def event_form(request, usr_id):
    form = EventModelForm()
    org_search_query = request.GET.get('search')
    organizers = User.objects.filter(groups__name="Organizer")

    if org_search_query:
        organizers = organizers.filter(username__icontains=org_search_query)
        
    if request.method == "POST":
        form = EventModelForm(request.POST, request.FILES)
        form.fields["organizers"].queryset = organizers
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            form.save_m2m()
            event.organizers.add(User.objects.get(id=usr_id))
            messages.success(request, "Event created successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Something went wrong.")
    else :            
        form.fields["organizers"].queryset = organizers

    context = {
        "form": form,
        # "title": "Add a New Event",
        "orgs": org_search_query
    }

    return render(request, "event-form.html", context)

@login_required(login_url="error-405")
@user_passes_test(lambda u: is_admin(u) or is_Organizer(u), login_url="home")
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    form = EventModelForm(instance=event)
    org_search_query = request.GET.get('search')
    organizers = User.objects.filter(groups__name="Organizer")

    if org_search_query:
        organizers = organizers.filter(username__icontains=org_search_query)
        
    if request.method == "POST":
        form = EventModelForm(request.POST,request.FILES, instance=event)
        form.fields["organizers"].queryset = organizers
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Something went wrong.")
    else :            
        form.fields["organizers"].queryset = organizers

    context = {
        "form": form,
        "title": "Edit Event",
        "orgs": org_search_query
    }

    return render(request, "event-form.html", context)

@login_required(login_url="error-405")
@user_passes_test(lambda u: is_admin(u) or is_Organizer(u), login_url="home")
def delete_event(request, event_id):
    """
    next_url places the current active url after deletion
    """
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))

    try:
        event = Event.objects.get(id=event_id)
        event.delete()
        messages.success(request, "Event deleted successfully!")
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")

    # print(next_url)
    return redirect(next_url)


@login_required(login_url="error-405")
def rsvp_event(request, event_id):

    next_url = request.GET.get('next', 'dashboard')
    event = Event.objects.get(id=event_id)
    current_date = date.today()
    rsvp_ins = RSVP.objects.select_related('event', 'participants', 'organizers')

    if event.date < current_date:
        messages.error(request, "Event ended")
    elif not rsvp_ins.filter(event__id=event_id, participants=request.user).exists():
        RSVP.objects.create(event = event, participants = request.user, is_going = False)
        messages.success(request, "Confirm RSVP by Clicking the link in your email")
    else :
        messages.error(request, "Please confirm your RSVP by clicking the link sent to your email.")

    return redirect(next_url)


@login_required(login_url="error-405")
def rsvp_removed(request, event_id):
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))

    rsvp_ins = RSVP.objects.filter(
        Q(participants=request.user) | Q(event__organizers=request.user),
        event__id=event_id
    )
    
    if rsvp_ins.exists():
        rsvp_ins.delete()
        messages.success(request, "RSVP Removed") 
    else :
        messages.error(request, "Not yet RSVP")

    return redirect(next_url)

@login_required(login_url="error-405")
def rsvp_activation(request, uid, token):
    try:
        rsvp = RSVP.objects.get(id = uid)
        if default_token_generator.check_token(rsvp.participants, token):
            rsvp.is_going = True
            rsvp.save()
            messages.success(
                request,
                "Successfully RSVP the event"
            )
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid activation")
            return redirect('dashboard')
    except RSVP.DoesNotExist:
        messages.error(request, "Invalid Activation Link")
        return redirect("dashboard")


