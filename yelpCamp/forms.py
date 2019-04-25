from django import forms

class NewCampgroundForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    imageUrl = forms.URLField(
        label='',
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image Url'}))
    description = forms.CharField(
        label='',
        max_length=1000,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
