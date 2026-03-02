from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # User
    path('s-inscrire/', views.register, name='register'),
    path('se-connecter/', views.user_login, name='login'),
    path('se-deconnecter/', views.user_logout, name='logout'),
    path('mon-compte/', views.my_account, name='my_account'),

    # Admin redirect
    path('', views.admin_redirect, name='admin_redirect'),
    # Admin
    path('administrateur/', views.admin_index, name='admin_index'),

    # Password change
    path('nouveau-mot-de-passe/', views.change_password, name="change_password"),

    # Messages de contact
    path('messages/',              views.contact_messages,       name='contact_messages'),
    path('messages/<int:pk>/',     views.contact_message_detail, name='contact_message_detail'),
    path('messages/<int:pk>/supprimer/', views.contact_message_delete, name='contact_message_delete'),

    # Password reset
    path('reinitialiser-mot-de-passe/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset/password_reset_form.html'), name="password_reset"),
    path('reinitialiser-mot-de-passe/envoye/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset/password_reset_done.html'), name="password_reset_done"),
    path('reinitialiser/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset/password_reset_confirm.html'), name="password_reset_confirm"),
    path('reinitialiser/termine/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/password_reset_complete.html'), name="password_reset_complete"),
]
