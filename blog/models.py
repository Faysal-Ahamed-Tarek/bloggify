import uuid
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User




class Category(models.Model) : 
    name = models.CharField(max_length = 100, unique=True, db_index=True, verbose_name="Category Name")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="Category Slug")
    description = models.TextField(verbose_name="Category Description", blank=True)
    recommended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta : 
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self) -> str : 
        return self.name

    def save(self, *args, **kwargs) -> None : 
        if not self.slug :
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    

class Tag(models.Model) : 
    name = models.CharField(max_length = 100, unique=True, db_index=True, verbose_name="Tag Name")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="Tag Slug")
    description = models.TextField(verbose_name="Tag Description", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta : 
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
    
    def __str__(self) -> str : 
        return self.name

    def save(self, *args, **kwargs) -> None : 
        if not self.slug :
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class BlogPost(models.Model) : 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    featured_image = models.ImageField(upload_to="blogpost/featured_images/")
    content = models.TextField()
    excerpt = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="BlogPosts", db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "BlogPosts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="BlogPosts")

    related_blogs = models.ManyToManyField("self", blank = True, symmetrical=True, related_name="RelatedBlogs")

    views = models.PositiveIntegerField(default=0)
    is_feature = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=[("draft", "Draft"), ("published", "Published")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta : 
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def save(self, *args, **kwargs) -> None : 
        if not self.slug : 
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    
    def viewsCounter(self, request) -> None :
        session_key = f'viewed_post_{self.id}'
          
        if not request.session.get(session_key, False):
            BlogPost.objects.filter(id=self.id).update(views=models.F('views') + 1)
            request.session[session_key] = True
    
    def min_reading_time(self) -> int :
        words = self.content.split()
        word_count = len(words)
        reading_time = word_count // 100
        return max(reading_time, 1)
    
    def __str__(self) -> str :
        return self.title