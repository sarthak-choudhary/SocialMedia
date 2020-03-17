from django import forms
from django.contrib.auth.models import User
from Accounts.forms import UserCreateForm

 

class CommentForm(forms.Form):
    content = forms.CharField(required=True,widget=forms.Textarea(attrs={'class':'form-control','placeholder': 'Type your comment here'}))

class ProfileUpdateForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    profile_pic = forms.ImageField()
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=range(1980,2015)))
    about = forms.CharField(widget=forms.Textarea())

class NewPostForm(forms.Form):
    title = forms.CharField(required=True,
                            max_length=140,
                            widget=forms.TextInput(
                                attrs={'class':'form-control',
                                'placeholder':'Enter a Title'}))

    content = forms.CharField(required=True,
                              min_length=50,
                              max_length=2000,
                              widget=forms.Textarea(
                                attrs={'class':'form-control',
                                        'placeholder':'share your views'}))
