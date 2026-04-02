from django.contrib import admin
from django.contrib.sessions.models import Session
from blog.models import BlogPost, Category, Tag


class BlogPostAdmin(admin.ModelAdmin) : 
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category", "status", "created_at", "is_feature")
    search_fields = ("title", "content", "status", "category__name")
    list_editable = ("status", "is_feature")
    # list_filter = ("status", "is_feature", "category")

class CategoryAdmin(admin.ModelAdmin) : 
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "created_at")

class TagAdmin(admin.ModelAdmin) : 
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "created_at")    


class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'session_data', 'expire_date')
    readonly_fields = ('session_key', 'session_data', 'expire_date')


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Session, SessionAdmin)