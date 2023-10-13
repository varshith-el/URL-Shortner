from django import forms

class shortenedURLForm(forms.Form):
    url = forms.URLField(label = 'URL to Shorten')
    