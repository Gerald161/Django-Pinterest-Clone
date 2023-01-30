from rest_framework import serializers
from .models import Account
from django import forms


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["email", "password", "username"]


class App_change_details(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["email", "username", "password"]


class App_update(serializers.ModelSerializer):
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


class email_check(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email']

        def clean_email(self):
            if self.is_valid():
                email = self.cleaned_data['email']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
                except Account.DoesNotExist:
                    return email
                raise forms.ValidationError('Email "%s" is already in use.' % email)


class username_check(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username']

        def clean_username(self):
            if self.is_valid():
                username = self.cleaned_data['username']
                try:
                    account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
                except Account.DoesNotExist:
                    return username
                raise forms.ValidationError('Username "%s" is already in use.' % username)


class ChangePasswordSerializer(serializers.Serializer):
    model = Account

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)