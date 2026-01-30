from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def event_details(request):
    return render(request, 'event-details.html')
