from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Home & About
    path('', views.home_view, name='home'),
    path('home/', views.home_view, name='home_alias'),
    path('about/', views.about_view, name='about'),

    # Articles, Search & Categories
    path('posts/', views.post_list_view, name='post_list'),
    path('search/', views.search_view, name='search'),
    path('categories/', views.categories_list_view, name='categories_list'),
    path('category/<slug:slug>/', views.category_posts_view, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts_view, name='tag_posts'),

    # Author Studio & Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('author/<str:username>/', views.author_posts_view, name='author_posts'),

    # Post CRUD
    path('post/new/', views.post_create_view, name='post_create'),
    path('post/create/', views.post_create_view, name='post_create_alias'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete_view, name='post_delete'),
    path('post/<slug:slug>/toggle-status/', views.post_toggle_status_view, name='post_toggle_status'),

    # Comments
    path('comment/<int:pk>/delete/', views.comment_delete_view, name='comment_delete'),
]
