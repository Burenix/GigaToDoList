from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts.views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),

    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('confirm-email/<uidb64>/<token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email-confirmation-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
]