from .models import Category
from footer.models import aboutUs, socialLinks


def categories(request):
    return {
        'categories': Category.objects.all()
    }

def footer(request):
    return {
        'about_us': aboutUs.objects.first(),
        'social_links': socialLinks.objects.first()
    }