from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from django.views.generic import TemplateView, CreateView
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import redirect


from accounts.forms import UserForgotPasswordForm, UserPasswordChangeForm, UserRegisterForm, UserLoginForm, UserSetNewPasswordForm
from accounts.mixins import UserIsNotAuthenticated


User = get_user_model()

class UserLoginView(LoginView):
    """
    Авторизация на сайте
    """
    form_class = UserLoginForm
    template_name = 'accounts/user_login.html'
    next_page = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context
    
class UserRegisterView(UserIsNotAuthenticated, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('tasks')
    template_name = 'accounts/user_register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
        protocol = 'https' if self.request.is_secure() else 'http'
        activation_link = f"{protocol}://127.0.0.1:8000{activation_url}"
        try:
            send_mail(
                'Подтвердите свой электронный адрес',
                f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: {activation_link}',
                'jokeryt.fix@yandex.ru',
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            user.delete()
            form.add_error(None, 'Не удалось отправить письмо для подтверждения. Пожалуйста, попробуйте позже.')
            return self.form_invalid(form)
        return redirect('email_confirmation_sent')
    
class UserPasswordChangeView(PasswordChangeView):
    """
    Изменение пароля пользователя
    """
    form_class = UserPasswordChangeForm
    template_name = 'accounts/user_password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class UserForgotPasswordView(PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'accounts/user_password_reset.html'
    success_url = reverse_lazy('login')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлено на ваш email'
    subject_template_name = 'accounts/password_subject_reset_mail.txt'
    email_template_name = 'accounts/password_reset_mail.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context
    
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'accounts/user_password_set_new.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context
    
class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')
        
class EmailConfirmationSentView(TemplateView):
    template_name = 'accounts/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context
    
class EmailConfirmedView(TemplateView):
    template_name = 'accounts/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context
    
class EmailConfirmationFailedView(TemplateView):
    template_name = 'accounts/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context