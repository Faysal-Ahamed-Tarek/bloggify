from django.urls import include, path
from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("categories/", views.categories, name="categories"),
    path("blog/", views.blog, name="blog"),
    path("users/", views.users, name="users"),
    path("blog/add", views.add_blog, name="add_blog"),
    path("categories/add/", views.add_category, name="add_category"),
    path("blog/edit/<slug:slug>/", views.edit_blog, name="edit_blog"),
    path("blog/delete/<slug:slug>/", views.delete_blog, name="delete_blog"),
    path("categories/edit/<slug:slug>/", views.edit_category, name="edit_category"),
    path("categories/delete/<slug:slug>/", views.delete_category, name="delete_category"),
]