from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

# Class Based Views Import
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from events.models import Event,Category,RSVP
from events.forms import EventModelForm


# Checks
def is_admin(u):
    return u.groups.filter(name="Admin").exists()

def is_Organizer(u):
    return u.groups.filter(name="Organizer").exists()

def is_participant(u):
    return u.groups.filter(name="Participants").exists()

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
        
        return context
    
class event_detailsView(DetailView):
    model = Event 
    template_name  = "event-details.html"
    pk_url_kwarg = 'event_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.prefetch_related('rsvp__participants', 'organizers').get(id=self.object.pk) 
        context['event'] = events
        context['count'] = events.rsvp.aggregate(participants_cnt=Count('id')),
        return context

permission_decorators = [
    login_required(login_url="error-405"),
    user_passes_test(lambda u: is_admin(u) or is_Organizer(u), login_url="home")
]

@method_decorator(permission_decorators, name='dispatch')
class event_formView(CreateView):
    model = Event
    form_class = EventModelForm
    permissoin_required = 'events.add_event'
    success_url = reverse_lazy("dashboard")
    pk_url_kwarg = "usr_id"

    template_name = "event-form.html"
    
    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        search = self.request.GET.get("search")
        organizers = User.objects.filter(groups__name="Organizer")

        if search:
            organizers = organizers.filter(username__icontains=search)
        
        form.fields["organizers"].queryset = organizers

        return form
    
    def form_valid(self, form):
        usr_id = self.kwargs["usr_id"]

        event = form.save(commit=False)
        event.save()
        form.save_m2m()

        event.organizers.add(User.objects.get(id=usr_id))

        messages.success(self.request, "Event created successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong.")
        return super().form_invalid(form)
    
@method_decorator(permission_decorators, name='dispatch')
class edit_eventView(UpdateView):
    model = Event
    form_class = EventModelForm
    permission_required = "events.change_event"
    template_name = "event-form.html"
    pk_url_kwarg = "event_id"
    success_url = reverse_lazy("dashboard")

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        org_search_query = self.request.GET.get('search')
        organizers = User.objects.filter(groups__name="Organizer")

        if org_search_query:
            organizers = organizers.filter(username__icontains=org_search_query)

        form.fields["organizers"].queryset = organizers

        return form
    
    def form_valid(self, form):
        event = Event.objects.get(id = self.object.pk)
        form = EventModelForm(self.request.POST,self.request.FILES, instance=event)
        form.save()
        messages.success(self.request, "Event updated successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong.")
        response = super().form_invalid(form)
        return response
    
@method_decorator(permission_decorators, name='dispatch')
class delete_eventView(DeleteView):
    model = Event
    pk_url_kwarg = "event_id"
    template_name = None

    def form_valid(self, form):
        messages.success(self.request, "Event deleted successfully!")
        return super().form_valid(form)
    

    def get_success_url(self):
        return (
            self.request.POST.get("next")
            or self.request.GET.get("next")
            or reverse_lazy("dashboard")
        )


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


