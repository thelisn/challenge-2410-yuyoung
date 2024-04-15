from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm
from django.db.models import Q


# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }

    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)    
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/new.html', context)


def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    article.delete()
    return redirect('articles:index')



def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST': 
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/edit.html', context)

def search(request):
    query = request.GET.get('query')
    articles = []
    
    if query:
        articles = Article.objects.filter(
            Q(title__contains=query) |
            Q(content__contains=query) |
            Q(created_at__contains=query)
        )

    return render(request, 'articles/search.html', {'articles': articles})