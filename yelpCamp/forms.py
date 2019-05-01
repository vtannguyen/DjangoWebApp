from django import forms
from django.forms import ModelForm
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
