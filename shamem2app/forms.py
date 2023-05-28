from django import forms
from .models import Post, Tag
from datetime import datetime

class PostForm(forms.ModelForm):
    timeline_type = forms.ChoiceField(choices=Post.TIMELINE_CHOICES, widget=forms.Select)
    exact_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, datetime.now().year+1)), 
        required=False)
    decade = forms.ChoiceField(choices=[('', '---------')] + [(str(i), f'{i}s') for i in range(2010, 1890, -10)], required=False)
    season = forms.ChoiceField(choices=[('', '---------'), ('spring', 'Spring'), ('summer', 'Summer'), ('fall', 'Fall'), ('winter', 'Winter')], required=False)
    tags = forms.CharField(max_length=200, help_text="Enter comma-separated tags for this post.", required=False)
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'video','latitude', 'longitude', 'timeline_type', 'exact_date', 'decade', 'season','tags']

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            tags = self.cleaned_data['tags'].split(',')
            for tag_name in tags:
                tag_name = tag_name.strip()
                if tag_name:  # check if tag_name is not empty
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)
        return instance

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='', required=False)
    SEARCH_CHOICES = [
        ('user', 'User'),
        ('location', 'Location'),
        ('tag', 'Tag'),
        ('time', 'Time'),
    ]
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES, initial='user', widget=forms.RadioSelect, label='')

    # New fields for time search
    TIMELINE_CHOICES = [
        (None, '---------'),
        ('exact_date', 'Exact date'),
        ('decade', 'Decade'),
        ('season', 'Season'),
    ]
    timeline_type = forms.ChoiceField(choices=TIMELINE_CHOICES, required=False)
    timeline_query = forms.CharField(required=False)
