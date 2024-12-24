from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from users.forms import CustomUserCreationForm, CustomUserProfileForm
from users.models import Contact, Subscribers, CustomUser


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserProfileForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user


def add_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()

        return redirect('index')

    return redirect('index')


def add_subscriber(request):
    if request.method == 'POST':
        email = request.POST.get('EMAIL')
        subscriber = Subscribers(email=email)
        subscriber.save()
    return redirect('index')
