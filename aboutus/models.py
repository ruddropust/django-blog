from django.db import models

# Create your models here.

class About(models.Model):
    about_heading = models.CharField(max_length=25)
    about_description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'About'

    def __str__(self):
        return self.about_heading
    
class FollowUs(models.Model):
    platform_name = models.CharField(max_length=25)
    platform_link = models.URLField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = 'FollowUs'

    def __str__(self):
        return self.platform_name
