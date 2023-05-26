from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
#from taggit.managers import TaggableManager



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    # Add the new fields for timeline
    TIMELINE_CHOICES = [
        ('exact_date', 'Exact date'),
        ('decade', 'Decade'),
        ('season', 'Season'),
    ]
    timeline_type = models.CharField(max_length=15, choices=TIMELINE_CHOICES, default='exact_date')
    exact_date = models.DateField(null=True, blank=True)
    decade = models.CharField(max_length=5, null=True, blank=True)
    season = models.CharField(max_length=10, null=True, blank=True)

    # Existing fields
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE,
    )
    body = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)    #tags = TaggableManager(blank=True)
    #tags = models.CharField(max_length=200, blank=True)
    
    

    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


