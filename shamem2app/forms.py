from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    location = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'video', 'latitude', 'longitude', 'location']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='')
    SEARCH_CHOICES = [
        ('user', 'User'),
        ('location', 'Location'),
        ('tag', 'Tag'),
    ]
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES, initial='user', widget=forms.RadioSelect, label='')
