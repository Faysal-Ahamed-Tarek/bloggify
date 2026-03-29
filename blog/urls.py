from django.urls import path
from blog import views


urlpatterns = [
    path("", views.home, name="home"),
    path("blog-feed/", views.blog_feed, name="blog_feed"),
    path("category/<slug:slug>/", views.category, name="category"),
]