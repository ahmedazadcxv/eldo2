from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render,redirect
from django.views.generic import ListView
import random

from .forms import NewCommentForm, PostSearchForm
from .models import Category, Comment, Post,Page
from accounts.models import Profile


def home(request):

    all_posts = Post.newmanager.all() 
    paginator = Paginator(all_posts, 15) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    pins = Post.objects.filter( pin='home' )
    profileN = Profile.objects.filter(dr=True)
    return render(request, 'blog/index.html', {'posts': page_obj,'pins': pins, 'Category': Category.objects.all(),'profile': profileN })

def videos(request):

    all_posts = Post.newmanager.all().filter( video_or_article='video' )
    paginator = Paginator(all_posts, 15) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    pins = Post.objects.filter( pin='videos' )
    return render(request, 'blog/videos.html', {'posts': page_obj,'pins': pins, 'Category': Category.objects.all() })



def post_single(request, post):

    post = get_object_or_404(Post, slug=post, status='published')
    postcat = Post.objects.filter(category=post.category).exclude(id=post.id).order_by('?')[0:9]
    video_url = ''

    fav = bool
    random_items = Post.newmanager.all().order_by('?')[0:9]

    if post.favourites.filter(id=request.user.id).exists():
        fav = True
 
    session_key = 'view_post_{}'.format(post)
    if not request.session.get(session_key,False):
        post.views +=1
        post.save()
        request.session[session_key] = True
    
    if 'video' in post.video_or_article:
        video_url = post.video_url.split(",")[1]

        return render(request, 'blog/vSingle.html', {'post': post, 'random_items': random_items,'video_url': video_url,
        'Category': Category.objects.all(),'Category2': postcat, 
        'fav': fav})
    else:
        return render(request, 'blog/single.html', {'post': post, 'random_items': random_items,
        'Category': Category.objects.all(),'Category2': postcat, 
        'fav': fav})
 

def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
    except:
        instance = get_object_or_404(Post, slug = category_slug[-1])
        return render(request, "blog/single.html", {'instance':instance})
    else:
        return render(request, 'blog/category.html', {'instance':instance})
 


class bodyOrgans(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'pins':Post.objects.filter( pin='bodyOrgans' ),
            'cat':  Category.objects.get( slug=self.kwargs['bodyOrgans']),
            'posts': Post.objects.filter(category__slug=self.kwargs['bodyOrgans']).filter(status='published'),
            'Category': Category.objects.all(), 
            'Category11': Category.objects.get( slug=self.kwargs['bodyOrgans']).get_family()
            
        }
        return content





def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context



def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)

            results = Post.objects.filter(query)

    return render(request, 'blog/search.html',
                  {'form': form,
                   'q': q,
                   'results': results})


class page(ListView):
    template_name = 'blog/page.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'page':  Page.objects.get( slug=self.kwargs['page']) 
            
        }
        return content
 
 
def post_user(request, slug):
    

    post = get_object_or_404(Profile, slug=slug )
    all_posts = Post.objects.filter(author=post.user)


    paginator = Paginator(all_posts, 15) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    pins = Post.objects.filter( pin='home' )
    return render(request, 'blog/user_posts.html', {'posts': page_obj,'pins': pins, 'ProfileN': post })