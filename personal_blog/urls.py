from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blog import views as blog_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


def custom_logout_view(request):
    """
    User logout view supporting both GET and POST for seamless UX.
    """
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('blog:home')


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication routes
    path('register/', blog_views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),

    # Direct top-level aliases to support unprefixed URL names
    path('home/', blog_views.home_view, name='home_top'),
    path('about/', blog_views.about_view, name='about_top'),
    path('dashboard/', blog_views.dashboard_view, name='dashboard_top'),
    path('search/', blog_views.search_view, name='search_top'),
    path('categories/', blog_views.categories_list_view, name='categories_list_top'),

    # Include main blog URLs (provides 'blog:<name>' namespace and root path)
    path('', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
