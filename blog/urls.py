from django.urls import path
from blog import views


urlpatterns = [
    path("", views.home, name="home"),
    path("blog-feed/", views.blog_feed, name="blog_feed"),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("reading-list/", views.reading_list, name="reading_list"),
    path("reading-list/add/<slug:slug>/", views.add_to_reading_list, name="add_to_reading_list"),
    path("reading-list/delete/<slug:slug>/", views.delete_from_reading_list, name="delete_from_reading_list"),
    path("category/<slug:slug>/", views.category, name="category"),
    path("@<str:username>/<path:slug>/", views.blog_details, name="post_detail"),

]