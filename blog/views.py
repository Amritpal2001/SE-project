from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import (
        ListView, 
        DetailView , 
        CreateView, 
        UpdateView,
        DeleteView)
from .models import Post, Rating

def home(request) :
    
    context = {
        'posts' : Post.objects.all()
    }
    return render(request , 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html

    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User , username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def PostDetailView(request, id):
    post = get_object_or_404(Post, id=id)
    if(Rating.objects.filter(user = request.user , post = post).exists()):
        rating = Rating.objects.get(user = request.user , post = post)
        context = {
            'post' : post,
            'rating' : rating,
        }
    else:
        context = {
            'post' : post,
        }
    return render(request, 'blog/post_detail.html', context)
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['category','title' , 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title' , 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url='/'

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False


def about(request) :
    return render(request , 'blog/about.html' , { 'title' : 'About'})

@csrf_exempt
def addRating(request):
    if request.method == 'POST':
        post = Post.objects.get(id = request.POST.get('post_id'))
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        if(Rating.objects.filter(user = request.user , post = post).exists()):
            rating_obj = Rating.objects.get(user = request.user , post = post)
            rating_obj.rating = rating
            rating_obj.review = review
            rating_obj.save()
        else:
            rating_obj = Rating(user = request.user , post = post , rating = rating, review = review)
            rating_obj.save()
        return JsonResponse({'success':True})

