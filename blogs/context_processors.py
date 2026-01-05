from blogs.models import Category
from aboutus.models import FollowUs


def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)

def get_social_link(request):
    platforms = FollowUs.objects.all()
    return dict(platforms=platforms)