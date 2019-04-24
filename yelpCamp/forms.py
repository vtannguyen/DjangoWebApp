from django import forms

class NewCampgroundForm(forms.Form):
    name = forms.CharField(max_length=200)
    imageUrl = forms.URLField(max_length=400)
