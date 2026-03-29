from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from blog.models import Category, BlogPost


# Create your views here.
def home(request) : 
    categories = Category.objects.all()
    latest_posts = BlogPost.objects.select_related("author", "category").all().order_by("-created_at")[:6]
    context = {
        "categories": categories,
        "latest_posts": latest_posts
    }
    
    return render(request, "bloggify.html", context)


def category(request, slug) : 
    category = get_object_or_404(Category, slug=slug)
    blog_posts = BlogPost.objects.select_related("author", "category").filter(category=category).order_by("-created_at")
    context = {
        "category": category,
        "blog_posts": blog_posts,
        "categories": Category.objects.all(),
    }
    return render(request, "categoryBlog.html", context)


def blog_feed(request) :
    categories = Category.objects.all()
    posts = BlogPost.objects.select_related("author", "category").all().order_by("?")
    context = {
        "categories": categories,
        "posts": posts,
    }
    return render(request, "blogfeed.html", context)


def blog_details(request, username, slug) : 
    blog = get_object_or_404(BlogPost, slug=slug, author__username=username)
    categories = Category.objects.all()
    context = {
        "blog" : blog,
        "categories" : categories
    }
    return render(request, "blogDetail.html", context)