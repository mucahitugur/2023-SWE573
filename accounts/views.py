from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, UpdateProfileForm
from django.contrib.auth import login, update_session_auth_hash, authenticate


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = UpdateProfileForm(instance=request.user.userprofile)

    context = {'form': form}
    return render(request, 'update_profile.html', context)
