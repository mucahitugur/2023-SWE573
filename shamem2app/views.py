from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post, Follow
from .forms import PostForm, SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_yeni.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_edit.html"

class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_silme.html"
    success_url = reverse_lazy("home")

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    follow_obj, created = Follow.objects.get_or_create(
        follower=request.user,
        followed=user_to_follow
    )
    if not created:
        follow_obj.delete()
    return redirect(reverse('user_profile', args=[username]))

class UserProfileView(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        context['user_posts'] = Post.objects.filter(author=user)
        context['following'] = user.followers.filter(follower=self.request.user).exists()
        context['followers_count'] = user.followers.count()
        context['following_count'] = user.following.count()
        return context
    
class MyProfileView(DetailView):
    model = User
    template_name = 'user_profile.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_posts'] = Post.objects.filter(author=user)
        context['following_count'] = user.following.count()
        context['followers_count'] = user.followers.count()
        return context

# User search function
def search(request):
    query = request.GET.get('search')
    search_type = request.GET.get('search_type')
    user_results = []
    post_results = []

    if query:
        if search_type == 'user':
            user_results = User.objects.filter(Q(username__icontains=query))

        elif search_type == 'location':
            post_results = Post.objects.filter(Q(location__icontains=query))

        elif search_type == 'tag':
            post_results = Post.objects.filter(Q(tags__name__icontains=query)).distinct()

    form = SearchForm(request.GET or None)

    context = {
        'form': form,
        'user_results': user_results,
        'post_results': post_results,
    }

    return render(request, 'search.html', context)
