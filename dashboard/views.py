from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from blog.models import BlogPost, Category
from django.contrib.auth.decorators import login_required


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


def categories(request) : 
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, "dashboard/category.html", context)