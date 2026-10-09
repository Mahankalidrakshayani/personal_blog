from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Sum
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.http import HttpResponseForbidden

from .models import Post, Category, Tag, Comment, Profile
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    PostForm,
    CommentForm,
)
from django.contrib.auth.models import User


def home_view(request):
    """
    Homepage displaying hero section, featured post, categories,
    latest articles with pagination/preview, and author highlights.
    """
    # Featured post (marked as featured and published, or latest published)
    featured_post = (
        Post.objects.filter(status='published', is_featured=True).first()
        or Post.objects.filter(status='published').first()
    )

    # Latest posts excluding the hero post if present
    latest_posts_qs = Post.objects.filter(status='published')
    if featured_post:
        latest_posts_qs = latest_posts_qs.exclude(pk=featured_post.pk)

    # Categories with published count
    categories = Category.objects.annotate(
        num_posts=Count('posts', filter=Q(posts__status='published'))
    ).order_by('-num_posts')[:6]

    # Trending / most viewed posts
    trending_posts = (
        Post.objects.filter(status='published')
        .order_by('-views_count', '-published_at')[:4]
    )

    context = {
        'featured_post': featured_post,
        'latest_posts': latest_posts_qs[:6],
        'categories': categories,
        'trending_posts': trending_posts,
    }
    return render(request, 'blog/home.html', context)


def post_list_view(request):
    """
    Blog posts explore/archive view with keyword search, category & tag filters,
    sorting options, and pagination.
    """
    posts = Post.objects.filter(status='published')

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    tag_slug = request.GET.get('tag', '').strip()
    sort_by = request.GET.get('sort', 'latest').strip()

    active_category = None
    active_tag = None

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=active_category)

    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    if sort_by == 'popular':
        posts = posts.order_by('-views_count', '-published_at')
    elif sort_by == 'oldest':
        posts = posts.order_by('published_at')
    else:
        # Default: latest
        posts = posts.order_by('-published_at', '-created_at')

    # Pagination: 6 posts per page
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    context = {
        'page_obj': page_obj,
        'query': query,
        'active_category': active_category,
        'active_tag': active_tag,
        'sort_by': sort_by,
        'total_results': posts.count(),
    }
    return render(request, 'blog/post_list.html', context)


def post_detail_view(request, slug):
    """
    Single blog post detail page with draft privacy protection,
    view counter increment, comment submission, and related posts.
    """
    post = get_object_or_404(Post, slug=slug)

    # Privacy enforcement for draft posts
    if post.status == 'draft':
        if not request.user.is_authenticated or (request.user != post.author and not request.user.is_staff):
            messages.warning(request, "This post is currently a draft and only viewable by its author.")
            return redirect('blog:home')

    # View counter: track viewed posts in user session to prevent refresh spam
    session_key = f'viewed_post_{post.pk}'
    if not request.session.get(session_key, False):
        Post.objects.filter(pk=post.pk).update(views_count=post.views_count + 1)
        post.refresh_from_db(fields=['views_count'])
        request.session[session_key] = True

    # Handle comment submission
    comment_form = CommentForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to join the conversation and leave a comment.")
            return redirect(f"{redirect('login').url}?next={post.get_absolute_url()}")

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment has been posted successfully!")
            return redirect('blog:post_detail', slug=post.slug)

    # Related posts (from same category, excluding current post)
    related_posts = []
    if post.category:
        related_posts = Post.objects.filter(
            status='published',
            category=post.category
        ).exclude(pk=post.pk)[:3]

    # Next and Previous posts
    prev_post = Post.objects.filter(
        status='published',
        published_at__lt=post.published_at or post.created_at
    ).order_by('-published_at').first()

    next_post = Post.objects.filter(
        status='published',
        published_at__gt=post.published_at or post.created_at
    ).order_by('published_at').first()

    comments = post.comments.filter(is_approved=True).select_related('author', 'author__profile')

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
        'prev_post': prev_post,
        'next_post': next_post,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create_view(request):
    """
    Create a new blog post. Only authenticated users can access.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(author=request.user)
            if post.status == 'published':
                messages.success(request, f"'{post.title}' has been published successfully!")
                return redirect('blog:post_detail', slug=post.slug)
            else:
                messages.info(request, f"Draft saved for '{post.title}'. You can find it in your Author Dashboard.")
                return redirect('blog:dashboard')
    else:
        form = PostForm()

    context = {
        'form': form,
        'title': 'Create New Blog Post',
        'submit_btn': 'Publish Post',
        'is_create': True,
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def post_edit_view(request, slug):
    """
    Edit an existing blog post. Only the post author or staff can edit.
    """
    post = get_object_or_404(Post, slug=slug)

    # Authorization check
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "Permission denied. You can only edit your own posts.")
        return redirect('blog:dashboard')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(author=post.author)
            messages.success(request, f"Changes saved for '{post.title}'.")
            if post.status == 'published':
                return redirect('blog:post_detail', slug=post.slug)
            else:
                return redirect('blog:dashboard')
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'title': f"Edit Post: {post.title}",
        'submit_btn': 'Save Changes',
        'is_create': False,
    }
    return render(request, 'blog/post_form.html', context)


@login_required
def post_delete_view(request, slug):
    """
    Delete a blog post with confirmation. Only author or staff permitted.
    """
    post = get_object_or_404(Post, slug=slug)

    # Authorization check
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "Permission denied. You can only delete your own posts.")
        return redirect('blog:dashboard')

    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f"Post '{post_title}' was successfully deleted.")
        return redirect('blog:dashboard')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def post_toggle_status_view(request, slug):
    """
    Quickly toggle post status between 'draft' and 'published' from author dashboard.
    """
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "Permission denied.")
        return redirect('blog:dashboard')

    if post.status == 'published':
        post.status = 'draft'
        messages.info(request, f"'{post.title}' has been moved to drafts.")
    else:
        post.status = 'published'
        if not post.published_at:
            post.published_at = timezone.now()
        messages.success(request, f"'{post.title}' is now live and published!")

    post.save()
    return redirect('blog:dashboard')


@login_required
def dashboard_view(request):
    """
    Personal author dashboard showing stats, metrics, and personal post management.
    """
    user = request.user
    user_posts = Post.objects.filter(author=user).select_related('category')

    # Status filter tab
    status_filter = request.GET.get('status', 'all')
    search_q = request.GET.get('q', '').strip()

    filtered_posts = user_posts
    if status_filter in ['published', 'draft']:
        filtered_posts = filtered_posts.filter(status=status_filter)

    if search_q:
        filtered_posts = filtered_posts.filter(
            Q(title__icontains=search_q) |
            Q(summary__icontains=search_q)
        )

    # Metrics calculation
    total_posts = user_posts.count()
    published_count = user_posts.filter(status='published').count()
    draft_count = user_posts.filter(status='draft').count()
    total_views = user_posts.aggregate(Sum('views_count'))['views_count__sum'] or 0
    total_comments = Comment.objects.filter(post__author=user, is_approved=True).count()

    # Pagination for dashboard posts
    paginator = Paginator(filtered_posts.order_by('-updated_at'), 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'total_posts': total_posts,
        'published_count': published_count,
        'draft_count': draft_count,
        'total_views': total_views,
        'total_comments': total_comments,
        'status_filter': status_filter,
        'search_q': search_q,
        'page_obj': page_obj,
    }
    return render(request, 'blog/dashboard.html', context)


def category_posts_view(request, slug):
    """
    List posts belonging to a specific category.
    """
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-published_at')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'total_count': posts.count(),
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts_view(request, slug):
    """
    List posts tagged with a specific tag.
    """
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published').order_by('-published_at')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tag': tag,
        'page_obj': page_obj,
        'total_count': posts.count(),
    }
    return render(request, 'blog/tag_posts.html', context)


def author_posts_view(request, username):
    """
    Public author profile page with bio and published articles.
    """
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author, status='published').order_by('-published_at')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    profile = getattr(author, 'profile', None)

    context = {
        'author_user': author,
        'profile': profile,
        'page_obj': page_obj,
        'total_count': posts.count(),
    }
    return render(request, 'blog/author_posts.html', context)


@login_required
def comment_delete_view(request, pk):
    """
    Delete a comment. Allowed for comment author or the post author.
    """
    comment = get_object_or_404(Comment, pk=pk)
    post_slug = comment.post.slug

    # Permission check: comment author, post author, or staff
    if comment.author != request.user and comment.post.author != request.user and not request.user.is_staff:
        messages.error(request, "Permission denied to remove this comment.")
        return redirect('blog:post_detail', slug=post_slug)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment removed.")

    return redirect('blog:post_detail', slug=post_slug)


def register_view(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('blog:dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f"Welcome to My Personal Blog, {username}! Your author account is ready.")
            return redirect('blog:dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request):
    """
    User profile settings: update name, email, bio, headline, avatar, and social links.
    """
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile details have been updated successfully!")
            return redirect('blog:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/profile.html', context)


def about_view(request):
    """
    About page providing blog overview, author background, tech stack, and goals.
    """
    admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    categories_count = Category.objects.count()
    posts_count = Post.objects.filter(status='published').count()
    authors_count = User.objects.count()

    context = {
        'admin_user': admin_user,
        'categories_count': categories_count,
        'posts_count': posts_count,
        'authors_count': authors_count,
    }
    return render(request, 'blog/about.html', context)


def categories_list_view(request):
    """
    List of all categories with post counts, descriptions, and color badges.
    """
    categories = Category.objects.annotate(
        num_posts=Count('posts', filter=Q(posts__status='published'))
    ).order_by('-num_posts', 'name')

    return render(request, 'blog/categories_list.html', {'categories': categories})


def search_view(request):
    """
    Search route alias redirecting or handling search queries seamlessly.
    """
    return post_list_view(request)

