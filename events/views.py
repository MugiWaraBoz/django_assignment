from django.shortcuts import render
from events.models import Participant,Event,Category
from events.forms import EventModelForm

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def event_details(request):
    return render(request, 'event-details.html')

def event_form(request):
    category = Category.objects.all()
    participants = Participant.objects.all()
    form = EventModelForm()

    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()
    
    context = {
        "form": form,
    }

    return render(request, "event-form.html", context)