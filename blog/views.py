from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from blog.models import Category


# Create your views here.
def home(request) : 
    categories = Category.objects.all()
    context = {
        "categories": categories    
    }
    
    return render(request, "bloggify.html", context)


def category(request, slug) : 
    category = get_object_or_404(Category, slug=slug)
    return HttpResponse(f"Category: {category.name}")