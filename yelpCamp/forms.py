from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Campground, Comment


class NewCampgroundForm(ModelForm):
    class Meta:
        model = Campground
        fields = ['name', 'imageUrl', 'description', 'price']

    def __init__(self, *args, **kwargs):
        super(NewCampgroundForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'formField', 'placeholder': key})


class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(NewCommentForm, self).__init__(*args, **kwargs)

        self.fields['text'].label = ''
        self.fields['text'].widget.attrs.update({'class': 'formField', 'placeholder': 'comment'})


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
