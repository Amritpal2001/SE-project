from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import numpy as np
import pandas as pd
import sklearn

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


# def ML_algo():
#     data = {'id':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28',
# '29','30','31','32','33','34','35','36','37','38','39','40'],
#         'rating':['4','5','2','3','1','5','4','1','3','2','4',
# '1','2','3','2','5','5','4','1','5','2','4','3','1','5','2','4','4','3','3','5','1','2','4','5','4','2',
# '2','1','3'] , 
#         'review' :['good','bad','bad','good','good','good','bad','good','bad','bad','bad','good','good','good','good'
# ,'bad','good','bad','bad','good','bad','bad','good','bad','good','bad','good','bad','good','good','good','bad'
# ,'good','bad','bad','good','good','bad','good','bad']
#        }
#     d = pd.DataFrame.from_dict(data)
#     d.head()
#     from sklearn.feature_extraction.text import TfidfVectorizer


#     tfv = TfidfVectorizer(min_df=3,  max_features=None, 
#                 strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
#                 ngram_range=(1, 3),
#                 stop_words = 'english')

#     # Filling NaNs with empty string
#     #movies_cleaned_df['overview'] = movies_cleaned_df['overview'].fillna('')

#     from sklearn.metrics.pairwise import sigmoid_kernel

#     # Compute the sigmoid kernel
#     sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
#     highestrated = []
#     val = 0
#     for i in d.rating:
#         if int(i)>val:
#             val = int(i)

#     j = 0
#     for i in d.rating:
#         if val == int(i):
#             highestrated.append(j)
#         j = j+1

#     l = []
#     for i in highestrated:
#         l = l + give_rec(i)

#     # def give_rec(title, sig=sig):
#         # Get the index corresponding to original_title
#     idx = int(title)

#     # Get the pairwsie similarity scores 
#     sig_scores = list(enumerate(sig[idx]))

#     # Sort the movies 
#     sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

#     # Scores of the 10 most similar movies
#     sig_scores = sig_scores[1:5]

#     # Movie indices
#     movie_indices = [i[0] for i in sig_scores]

#     # Top 10 most similar movies
#     #d['id'].iloc[movie_indices]
#     return movie_indices

def PostListView(request):
    posts = Post.objects.all().order_by('-date_posted')
    postML=[]
    final_posts = []
    if request.user.is_authenticated:
        postML = Rating.objects.filter(user=request.user)
        
        posts_list=[]
        for i in postML:
            posts_dict={}
            posts_dict['id']=i.post.id
            posts_dict['rating']=i.rating
            posts_dict['review']=i.review
            posts_list.append(posts_dict)
        # ML_algo()
        filter_li = [24, 28,30]
        
        for i in filter_li:
            post = Post.objects.get(id=i)
            final_posts.append(post)

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'final_posts':final_posts
    }
    return render(request, 'blog/home.html', context)
    

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

