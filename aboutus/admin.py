from django.contrib import admin
from .models import About, FollowUs
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin



class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
        'is_active',
        'get_groups',   # 👈 custom method
    )

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    get_groups.short_description = 'Groups'  # column name



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
# Unregister default User
admin.site.unregister(User)

# Register with customization
admin.site.register(User, CustomUserAdmin)