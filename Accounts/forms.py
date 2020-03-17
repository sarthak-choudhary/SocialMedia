from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class UserCreateForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=range(1980,2015)))
    username = forms.CharField(min_length=5)
    email = forms.EmailField()
    password1 = forms.CharField(min_length=8,widget = forms.PasswordInput())
    password2 = forms.CharField(min_length=8,widget = forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data
             
        if not (self.data['password1'] == self.data['password2']):
            raise ValidationError("Passwords did not match!")
