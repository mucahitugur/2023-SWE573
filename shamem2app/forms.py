from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    # Add the new fields for timeline
    timeline_type = forms.ChoiceField(choices=Post.TIMELINE_CHOICES, widget=forms.Select)
    exact_date = forms.DateField(widget=forms.SelectDateWidget, required=False)
    decade = forms.ChoiceField(choices=[('', '---------')] + [(str(i), f'{i}s') for i in range(2010, 1890, -10)], required=False)
    season = forms.ChoiceField(choices=[('', '---------'), ('spring', 'Spring'), ('summer', 'Summer'), ('fall', 'Fall'), ('winter', 'Winter')], required=False)

    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'video', 'latitude', 'longitude', 'tags', 'timeline_type', 'exact_date', 'decade', 'season']

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='')
    SEARCH_CHOICES = [
        ('user', 'User'),
        ('location', 'Location'),
        ('tag', 'Tag'),
    ]
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES, initial='user', widget=forms.RadioSelect, label='')
