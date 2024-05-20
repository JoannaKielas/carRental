

from django import forms
from rezerwacje.models import Auto, MyAccountManager, Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

TRANSMISSION_FORM_CHOICES = [("", "-------")] + Auto.TRANSMISSION_CHOICES
TYPE_FORM_CHOICES = [("", "-------")] + Auto.TYPE_CHOICES

class AutoForm(forms.ModelForm):
    type = forms.ChoiceField(choices=TYPE_FORM_CHOICES, required=False)
    price = forms.IntegerField(min_value=200, max_value=1000, required=False)
    seats = forms.IntegerField(min_value=2, max_value=9, required=False)
    transmission = forms.ChoiceField(choices=TRANSMISSION_FORM_CHOICES, required=False)

    class Meta:
        model = Auto
        fields = ["type", "price", "seats", "transmission"]

#forms for user registration
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Add email address")

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email{email} already exists')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username{username} already exists')

# forms for user login
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")


    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")





