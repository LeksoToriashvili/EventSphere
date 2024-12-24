from django import forms

from users.models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_organizer', 'is_attendee', 'password', 'password2', 'image')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("The two password fields must match.")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        is_organizer = cleaned_data.get('is_organizer')
        is_attendee = cleaned_data.get('is_attendee')

        if not (is_organizer or is_attendee):
            raise forms.ValidationError("You must select at least one role(Organizer or Attendee).")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_organizer', 'is_attendee', 'image']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }
