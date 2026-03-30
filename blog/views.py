from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from blog.forms import registration
from blog.models import Category, BlogPost
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

    context = {"blog": blog, "related_blogs": blog.related_blogs.all()}
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
            return redirect("register")
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
                return redirect("home")
    else :     
        form = AuthenticationForm()
    print(request.user.is_authenticated)
    return render(request, "login.html", {"form": form})



def logout(request):
    auth_logout(request)
    return redirect("login")