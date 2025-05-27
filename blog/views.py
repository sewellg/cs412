from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.

class ShowAllView(ListView):
    '''define view class to show all articles'''

    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

class ArticleView(DetailView):
    '''display single article'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article' # only one article shown at a time, hence singular

class RandomArticleView(DetailView):
    '''display random article'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article' # only one article shown at a time, hence singular

    # methods
    def get_object(self):
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
