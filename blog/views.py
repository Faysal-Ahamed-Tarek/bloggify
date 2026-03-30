from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from blog.models import Category, BlogPost
from django.db.models import Q

# Create your views here.
def home(request) : 
    latest_posts = BlogPost.objects.select_related("author", "category").all().order_by("-created_at")[:6]
    context = {
        "latest_posts": latest_posts
    }
    
    return render(request, "bloggify.html", context)


def category(request, slug) : 
    category = get_object_or_404(Category, slug=slug)
    blog_posts = BlogPost.objects.select_related("author", "category").filter(category=category).order_by("-created_at")
    context = {
        "category": category,
        "blog_posts": blog_posts,
    }
    return render(request, "categoryBlog.html", context)


def blog_feed(request) :
    posts = BlogPost.objects.select_related("author", "category").all().order_by("?")
    context = {
        "posts": posts,
    }
    return render(request, "blogfeed.html", context)


def blog_details(request, username, slug) : 
    blog = get_object_or_404(BlogPost, slug=slug, author__username=username)
    
    context = {
        "blog" : blog,
        "related_blogs": blog.related_blogs.all()
    }
    return render(request, "blogDetail.html", context)


def search(request) :
    query = request.GET.get("keyword", "")
    blog = BlogPost.objects.select_related("author", "category").filter(Q(title__icontains=query) | Q(category__name__icontains=query)).order_by("-created_at") 
    context = {
        "query": query,
        "blog_posts": blog,
    }
    return render(request, "search.html", context)