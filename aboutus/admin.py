from django.contrib import admin
from .models import About, FollowUs


class AboutAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        count = About.objects.all().count()
        if count==0:
            return True
        return False
class FlowUsAdmin(admin.ModelAdmin):
    list_display = ['platform_name','platform_link','is_published']
    list_editable = ['is_published']

# Register your models here.
admin.site.register(About, AboutAdmin)
admin.site.register(FollowUs,FlowUsAdmin)