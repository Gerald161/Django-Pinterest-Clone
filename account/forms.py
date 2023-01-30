from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        model = Account
        fields = ("email", "username")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            username = self.cleaned_data['username']

            try:
                account = Account.objects.get(email=email.lower())
                raise forms.ValidationError("Email already exists")
            except ObjectDoesNotExist:
                pass

            try:
                account = Account.objects.get(username=username.lower())
                raise forms.ValidationError("Username already exists")
            except ObjectDoesNotExist:
                pass


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            try:
                account = Account.objects.get(email=email.lower())
                if not authenticate(email=email.lower(), password=password):
                    raise forms.ValidationError("Password is wrong")
            except ObjectDoesNotExist:

                raise forms.ValidationError("Email Does Not Exist")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username')

        def clean_email(self):
            if self.is_valid():
                email = self.cleaned_data['email']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
                except Account.DoesNotExist:
                    return email
                raise forms.ValidationError('Email "%s" is already in use.' % email)

        def clean_username(self):
            if self.is_valid():
                username = self.cleaned_data['username']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
                except Account.DoesNotExist:
                    return username
                raise forms.ValidationError('Username "%s" is already in use.' % username)