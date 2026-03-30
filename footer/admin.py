from django.contrib import admin
from footer.models import aboutUs, socialLinks


class aboutUsAdmin(admin.ModelAdmin) :
    if aboutUs.objects.count() >= 1 : 
        def has_add_permission(self, request) :
            return False


class socialLinksAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        try:
            return socialLinks.objects.count() < 1
        except Exception:
            return True


# Register your models here.
admin.site.register(aboutUs, aboutUsAdmin)
admin.site.register(socialLinks, socialLinksAdmin)