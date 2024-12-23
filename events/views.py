from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from events.forms import EventForm
from events.models import Event


def index(request):
    print(request.GET.get('q'))
    return render(request, 'index.html')


def event_list(request):
    query = request.GET.get('q', '')
    date = request.GET.get('date', '')
    address_filter = request.GET.get('address', '')
    end_date = request.GET.get('end_date', '')
    print(end_date)

    events = Event.objects.filter(canceled=False).order_by('date')

    if query:
        events = events.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if date:
        if end_date:
            events = events.filter(date__range=(date, end_date))
        else:
            events = events.filter(date__date=date)

    if address_filter:
        events = events.filter(address__icontains=address_filter)

    return render(request, 'event_list.html', {
        'events': events,
        'query': query,
        'date_filter': date,
        'address_filter': address_filter,
        'end_date': end_date,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'event_create.html', {'form': form})


@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user in event.attendees.all():
        event.attendees.remove(request.user)
    else:
        event.attendees.add(request.user)
    return redirect('event_detail', event_id=event.id)


@login_required
def user_dashboard(request):
    organized_events = Event.objects.filter(organizer=request.user)
    attending_events = Event.objects.filter(attendees=request.user)
    context = {
        'organized_events': organized_events,
        'attending_events': attending_events,
    }
    return render(request, 'user_dashboard.html', context)
