from django.db import models

# Create your models here.
class aboutUs(models.Model) : 
    description = models.CharField(max_length=300)
    copyright = models.CharField(max_length=200)

    class Meta : 
        verbose_name_plural = "About Us"

    def __str__(self) : 
        return self.description[:50] + "..." if len(self.description) > 50 else self.description

class socialLinks(models.Model) : 
    facebook = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    youtube = models.CharField(max_length=100)

    class Meta : 
        verbose_name_plural = "Social Links"

    def __str__(self) : 
        return f"Social Links"