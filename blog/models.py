from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    review = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return str(self.rating)

class Post(models.Model) :
    category = models.ManyToManyField(Category, related_name='posts', blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now )
    author = models.ForeignKey( User , on_delete=models.CASCADE)

    def __str__(self) :
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk' : self.pk})


