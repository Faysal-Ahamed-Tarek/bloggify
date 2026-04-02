from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from blog.forms import commentForm, registration
from blog.models import Category, BlogPost, Comments, ReadLaterBlog
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout


# Create your views here.
def home(request):
    latest_posts = (
        BlogPost.objects.select_related("author", "category")
        .all()
        .order_by("-created_at")[:6]
    )
    
    context = {"latest_posts": latest_posts}

    return render(request, "bloggify.html", context)


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    blog_posts = (
        BlogPost.objects.select_related("author", "category")
        .filter(category=category)
        .order_by("-created_at")
    )
    context = {
        "category": category,
        "blog_posts": blog_posts,
    }
    return render(request, "categoryBlog.html", context)


def blog_feed(request):
    posts = BlogPost.objects.select_related("author", "category").all().order_by("?")
    
    context = {
        "posts": posts,
    }
    return render(request, "blogfeed.html", context)


def blog_details(request, username, slug):
    blog = get_object_or_404(BlogPost, slug=slug, author__username=username)
    comments = Comments.objects.select_related("user").filter(blog=blog).order_by("-created_at")
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            messages.success(request, "Your comment has been posted.")
            return redirect("post_detail", username=username, slug=slug)
        else :
            messages.error(request, "There was an error with your comment. Please try again.")
    else:
        form = commentForm()
        
    blog.viewsCounter(request)
    context = {"blog": blog, "related_blogs": blog.related_blogs.all(), "form": form, "comments": comments}
    return render(request, "blogDetail.html", context)


def search(request):
    query = request.GET.get("keyword", "")
    blog = (
        BlogPost.objects.select_related("author", "category")
        .filter(Q(title__icontains=query) | Q(category__name__icontains=query))
        .order_by("-created_at")
    )
    context = {
        "query": query,
        "blog_posts": blog,
    }
    return render(request, "search.html", context)


def register(request):
    if request.method == "POST":
        form = registration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = registration()
    context = {"form": form}
    return render(request, "register.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "You have been logged in successfully.")
                return redirect("dashboard")
    else:
        form = AuthenticationForm()
    print(request.user.is_authenticated)
    return render(request, "login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("login")


def reading_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your reading list.")
        return redirect("login")

    blog = (
        ReadLaterBlog.objects.select_related("blog", "blog__author")
        .filter(user=request.user)
        .order_by("-saved_at")
    )
    context = {
        "blog": blog,
    }
    return render(request, "readingList.html", context)


def add_to_reading_list(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    user = request.user

    if not user.is_authenticated:
        messages.error(request, "You need to be logged in to add to reading list.")
        return redirect("login")

    if ReadLaterBlog.objects.filter(user=user, blog=blog).exists():
        messages.info(request, "This blog is already in your reading list.")
        return redirect("post_detail", username=blog.author.username, slug=blog.slug)

    ReadLaterBlog.objects.create(user=user, blog=blog)
    messages.success(request, "Blog added to your reading list.")
    return redirect("reading_list")


def delete_from_reading_list(request, slug):
    blog = get_object_or_404(ReadLaterBlog, blog__slug=slug, user=request.user)
    blog.delete()
    messages.success(request, "Blog removed from your reading list.")
    return redirect("reading_list")
