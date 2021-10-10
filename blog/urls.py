from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from accounts.views import myaccount,profile
from accounts.views import email_list_signup


from posts.views import (
    index, blog, post, search, 
    post_create, post_update, post_delete,contact,faq)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name='index'),

    path('register/', accounts_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='accounts/logout.html'),name='logout'),
    path('account/',myaccount,name='myaccount'),



    path('password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'
    ),
    name='password_reset'),
path('password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ),
    name='password_reset_done'),
path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ),
    name='password_reset_confirm'),
path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ),
    name='password_reset_complete'),






    path('account/profile/',profile,name='profile'),
    path('subscribe/',email_list_signup,name='subscribe'),
    path('blog/', blog, name='post-list'),
    path('contact/',contact,name='contact'),
    path('search/', search, name='search'),
    path('faq/',faq,name='faq'),
    path('create/', post_create, name='post-create'),
    path('post/<id>/', post, name='post-detail'),
    path('post/<id>/update/', post_update, name='post-update'),
    path('post/<id>/delete/', post_delete, name='post-delete'),
    path('tinymce/', include('tinymce.urls')),
    path('oauth/',include('social_django.urls'),name='"social'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)