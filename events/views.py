from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DeleteView

from events.forms import EventForm
from events.models import Event
from notifications.models import Notification
from notifications.tasks import send_notification


def index(request):
    random_events = Event.objects.order_by('?')[:6]
    return render(request, 'index.html', {'events': random_events})


@cache_page(60 * 60 * 24)
def contact(request):
    return render(request, 'contact.html')


class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(canceled=False).order_by('date')

        query = self.request.GET.get('q', '')
        date = self.request.GET.get('date', '')
        address_filter = self.request.GET.get('address', '')
        end_date = self.request.GET.get('end_date', '')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))

        if date:
            if end_date:
                queryset = queryset.filter(date__range=(date, end_date))
            else:
                queryset = queryset.filter(date__date=date)

        if address_filter:
            queryset = queryset.filter(address__icontains=address_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['date_filter'] = self.request.GET.get('date', '')
        context['address_filter'] = self.request.GET.get('address', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees_count = event.attendees.count()
    liked = request.user in event.liked_by.all()
    return render(request, 'event_detail.html', {'event': event, 'attendees_count': attendees_count, 'liked': liked})


@login_required
def toggle_like(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.liked_by.all():
        event.liked_by.remove(request.user)
    else:
        event.liked_by.add(request.user)

    return redirect('event_detail', event_id=event.id)


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


class EventDeleteView(DeleteView):
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('user_dashboard')

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.organizer != self.request.user:
            raise PermissionDenied("You do not have permission to delete this Event.")
        return obj


class CancelEventView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        if event.organizer != request.user:
            raise PermissionDenied("You do not have permission to cancel this Event.")

        event.canceled = True
        event.save()
        send_notification.delay(Notification.EVENT_CANCELLED, event.id)

        return redirect('user_dashboard')


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
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    context = {
        'organized_events': organized_events,
        'attending_events': attending_events,
        'notifications': notifications,
    }
    return render(request, 'user_dashboard.html', context)
