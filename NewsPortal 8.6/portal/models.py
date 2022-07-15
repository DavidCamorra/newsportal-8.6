from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


news = 'news'
post = 'post'
POSTTYPES = [(news, 'Новости'), (post, 'Статья')]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_rating = models.FloatField(default=0)

    def update_rating(self, new_rating):
        self.rating = new_rating
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory', null=True)

    def __str__(self):
        return f'{self.name}'


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    post_auth = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=4, choices=POSTTYPES, default=news)
    add_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    name = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return f'{self.name} by {self.post_auth}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

