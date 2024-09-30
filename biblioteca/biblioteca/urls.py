"""
URL configuration for biblioteca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import (
    LogoutView, LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordChangeDoneView,
    PasswordResetCompleteView, PasswordChangeView)
from django.views.generic import TemplateView
from app.views import buscador, home, login_view, libros_prestados, prestar_ejemplar

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('base', TemplateView.as_view(template_name="app/base.html"), name='base'),

    # path('buscador', buscador, name='buscador'),

    path('libros-prestados', libros_prestados, name='libros-prestados'),

    path('prestar-ejemplar', prestar_ejemplar, name='prestar-ejemplar'),

    # path('login', LoginView.as_view(template_name="app/login_register.html", next_page="/"), name='login'),

    path('login', login_view, {'next_page': "/"}, name='login'),

    path('logout', LogoutView.as_view(next_page="/"), name='logout'),
    #
    path('olvide-mi-password', PasswordResetView.as_view(), name="password_reset"),

    path('olvide-mi-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
      template_name='auth/password_reset_confirm.html'), name="password_reset_confirm"),

    path('olvide-mi-password/hecho', PasswordResetDoneView.as_view(
      template_name='auth/password_reset_done.html'), name="password_reset_done"),

    path('olvide-mi-password/completo', PasswordResetCompleteView.as_view(
      template_name='auth/password_reset_complete.html'), name="password_reset_complete"),

    path('cambiar-password/', PasswordChangeView.as_view(
      template_name='auth/password_change_form.html'), name="password_change"),

    path('cambiar-password/completo', PasswordChangeDoneView.as_view(
      template_name='auth/password_change_complete.html'), name="password_change_done"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
