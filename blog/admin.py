from django.contrib import admin
from .models import Category, Tag, Post, Comment, Profile

admin.site.site_header = "My Personal Blog Admin Portal"
admin.site.site_title = "Blog Management"
admin.site.index_title = "Welcome to Blog Administration"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color', 'icon', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'views_count', 'published_at', 'created_at')
    list_filter = ('status', 'is_featured', 'category', 'published_at', 'created_at')
    search_fields = ('title', 'summary', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = ['make_published', 'make_draft']

    @admin.action(description="Mark selected posts as Published")
    def make_published(self, request, queryset):
        queryset.update(status='published')

    @admin.action(description="Mark selected posts as Draft")
    def make_draft(self, request, queryset):
        queryset.update(status='draft')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author__username', 'post__title', 'content')
    actions = ['approve_comments', 'disapprove_comments']

    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Disapprove selected comments")
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'website')
    search_fields = ('user__username', 'headline', 'bio')
