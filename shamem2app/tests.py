from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Follow
from django.contrib.auth.models import User

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Follow, Like, Comment

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.post = Post.objects.create(title='Test Post', author=self.user1, body='This is a test post.')

    def test_post_model(self):
        self.assertEqual(str(self.post), 'Test Post')
        self.assertEqual(self.post.get_absolute_url(), f'/post/{self.post.pk}/')

    def test_follow_model(self):
        follow = Follow.objects.create(follower=self.user1, followed=self.user2)
        self.assertEqual(str(follow), 'user1 follows user2')

    def test_like_model(self):
        like = Like.objects.create(user=self.user1, post=self.post)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(like.user, self.user1)
        self.assertEqual(like.post, self.post)

    def test_comment_model(self):
        comment = Comment.objects.create(user=self.user1, post=self.post, text='This is a comment.')
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.user, self.user1)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.text, 'This is a comment.')

        # Add more assertions to test the response, template used, context, etc.

        # Add more assertions to test the response, template used, context, etc.

    # Add more test methods to cover other views and their functionality

# Create your tests here.
