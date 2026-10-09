from .models import Category, Tag, Post
from django.db.models import Count

def blog_globals(request):
    """
    Context processor to inject shared blog variables across all templates.
    """
    try:
        categories = Category.objects.annotate(
            num_posts=Count('posts', filter=models_q_filter())
        ).order_by('-num_posts', 'name')[:8]
        popular_tags = Tag.objects.annotate(
            num_posts=Count('posts')
        ).order_by('-num_posts')[:12]
        recent_posts = Post.objects.filter(status='published').order_by('-published_at')[:4]
    except Exception:
        categories = []
        popular_tags = []
        recent_posts = []

    return {
        'global_categories': categories,
        'global_popular_tags': popular_tags,
        'global_recent_posts': recent_posts,
    }


def models_q_filter():
    from django.db.models import Q
    return Q(posts__status='published')
