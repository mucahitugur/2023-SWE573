from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'video', 'latitude', 'longitude']  # Add latitude and longitude here

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='')
    SEARCH_CHOICES = [
        ('user', 'User'),
        ('location', 'Location'),
        ('tag', 'Tag'),
    ]
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES, initial='user', widget=forms.RadioSelect, label='')
