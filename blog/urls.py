from django.urls import path
from blog import views


urlpatterns = [
    path("", views.home, name="home"),
    path("blog-feed/", views.blog_feed, name="blog_feed"),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("category/<slug:slug>/", views.category, name="category"),
    path("@<str:username>/<path:slug>/", views.blog_details, name="post_detail"),

]