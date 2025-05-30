from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import redirect

# Redirect root URL to login page
def root_redirect(request):
    return redirect('login')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='tracker/registration/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),  

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='tracker/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='tracker/password_change_done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('filter/', views.filter_by_body_type, name='filter_by_body_type'),
    path('report/', views.body_type_report, name='body_type_report'),

    path('', root_redirect),
]