from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from blog.models import BlogPost, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard.forms import BlogPostForm, categoryForm



# Create your views here.
@login_required(login_url="login")
def dashboard(request):
    blogCnt = BlogPost.objects.count()
    categoryCnt = Category.objects.count()
    writterCnt = User.objects.count()
    yourBlogCnt = BlogPost.objects.filter(author=request.user).count()

    context = {
        "blogCnt": blogCnt,
        "categoryCnt": categoryCnt,
        "writterCnt": writterCnt,
        "yourBlogCnt": yourBlogCnt,
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required(login_url="login")
def categories(request):
    return render(request, "dashboard/category.html")


@login_required(login_url="login")
def add_category(request):
    if request.method == "POST":
        form = categoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect("categories")
    else:
        form = categoryForm()
    context = {"form": form}
    return render(request, "dashboard/addCategory.html", context)


@login_required(login_url="login")
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect("categories")

@login_required(login_url="login")
def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        form = categoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("categories")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = categoryForm(instance=category)

    context = {"form": form, "category": category}
    return render(request, "dashboard/editCategory.html", context)


@login_required(login_url="login")
def blog(request):
    blogs = BlogPost.objects.all()
    context = {"blogs": blogs}
    return render(request, "dashboard/blog.html", context)


@login_required(login_url="login")
def add_blog(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            form.save_m2m()
            return redirect("blog")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BlogPostForm()
    context = {"form": form}
    return render(request, "dashboard/addBlog.html", context)


@login_required(login_url="login")
def edit_blog(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully.")
            return redirect("blog")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BlogPostForm(instance=blog_post)

    context = {"form": form, "blog_post": blog_post}
    return render(request, "dashboard/editBlog.html", context)

@login_required(login_url="login")
def delete_blog(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug)
    blog_post.delete()
    messages.success(request, "Blog post deleted successfully.")
    return redirect("blog")

@login_required(login_url="login")
def users(request):
    users = User.objects.all()
    context = {
        "users": users
    }
    return render(request, "dashboard/user.html", context)