from django import forms

class NewCampgroundForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    imageUrl = forms.URLField(
        label='',
        max_length=400,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image Url'}))
