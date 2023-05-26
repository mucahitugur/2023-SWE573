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
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Post, Like, Comment
from geopy.geocoders import Nominatim
from django.views import View
from .models import Post
from django.contrib.auth import login, update_session_auth_hash, authenticate


class BlogListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'

    def get_queryset(self):
        following_users = User.objects.filter(followers__follower=self.request.user)
        following_posts = Post.objects.filter(author__in=following_users)
        user_posts = Post.objects.filter(author=self.request.user)
        following_posts = following_posts.select_related('author').prefetch_related('like_set', 'comment_set')
        user_posts = user_posts.select_related('author').prefetch_related('like_set', 'comment_set')
        queryset = list(following_posts) + list(user_posts)
        return queryset

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

from django.core.exceptions import ValidationError

from django.core.exceptions import ValidationError

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post_new.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        latitude = form.cleaned_data.get('latitude')
        longitude = form.cleaned_data.get('longitude')
        if latitude and longitude:
            post.latitude = latitude
            post.longitude = longitude
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.reverse([latitude, longitude])
            post.location = location.address
        else:
            form.add_error(None, ValidationError("Please select a location on the map."))
            return self.form_invalid(form)
        post.save()
        #form.save_m2m()  
        return redirect('post_detail', pk=post.pk)



class BlogUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_edit.html"

class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
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

class PostsView(View):
    def get(self, request, tag_slug=None):
                if tag_slug:
                  posts = Post.objects.filter(tags__slug=tag_slug)
                else:
                  posts = Post.objects.all()
                return render(request, 'home.html', {'object_list': posts})


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

def search(request):
    query = request.GET.get('search')
    search_type = request.GET.get('search_type')

    print(f"Query: {query}")
    print(f"Search type: {search_type}")

    user_results = []
    post_results = []

    if query:
        if search_type == 'user':
            user_results = User.objects.filter(Q(username__icontains=query))
        elif search_type == 'location':
            post_results = Post.objects.filter(Q(location__icontains=query))
        elif search_type == 'tag':
            post_results = Post.objects.filter(Q(tags__name__icontains=query)).distinct()

    print(f"Post results: {post_results}")

    form = SearchForm(request.GET or None)

    context = {
        'form': form,
        'user_results': user_results,
        'post_results': post_results,
    }

    return render(request, 'search.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_likes = False

    if request.user.is_authenticated:
        user_likes = Like.objects.filter(post=post, user=request.user).exists()

    context = {
        'object': post,
        'user_likes': user_likes
    }

    return render(request, 'post_detail.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(user=request.user, post=post, text=text)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

