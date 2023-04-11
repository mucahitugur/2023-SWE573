from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True, update_profile_picture=False):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            if not update_profile_picture:
                profile = UserProfile(user=user)
                if 'profile_picture' in self.cleaned_data and self.cleaned_data['profile_picture']:
                    profile.profile_picture = self.cleaned_data['profile_picture']
                profile.save()
            else:
                user.userprofile.profile_picture = self.cleaned_data['profile_picture']
                user.userprofile.save()
        return user

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

