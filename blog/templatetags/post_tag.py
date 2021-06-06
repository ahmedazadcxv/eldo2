from django import template
from blog.models import Category,Post, Page 


register = template.Library()
@register.inclusion_tag('blog/latest_posts.html')
def latest_posts():
    context = {
        'l_posts': Category.objects.all()[0:15],
    }
    return context
  
@register.inclusion_tag('blog/v_posts.html')
def latest_posts1():
    context = {
        'l_posts': Post.objects.order_by('-views')[0:9],
    }
    return context
    
    
@register.inclusion_tag('blog/pageTag.html')
def pageTag():
    context = {
        'page': Page.objects.all()[0:15],
    }
    return context
  

@register.inclusion_tag('blog/silder.html')
def silder():
    context = {
        'l_posts': Category.objects.all()[0:15],
    }
    return context
   
@register.filter
def get_name(value):
    spam = value.split('/')[-1]         # assume value be /python/web-scrapping
                                        # spam would be 'web-scrapping'
    spam = ' '.join(spam.split('-'))    # now spam would be 'web scrapping'
    return spam