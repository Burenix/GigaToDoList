from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginForm(AuthenticationForm):
    """
    Форма авторизации на сайте
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы регистрации
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs['placeholder'] = 'Логин'
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль'
            self.fields['username'].label = ''
            self.fields['password'].label = ''
            self.fields[field].widget.attrs.update({
                'class': 'form-control-logpass-input',
                'autocomplete': 'off'
            })

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите свой email',
            'autocomplete': 'off',
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя',
            'autocomplete': 'off',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
            })
            if field == 'username':
                self.fields[field].widget.attrs.update({'placeholder': 'Придумайте свой логин'})
            elif field == 'email':
                self.fields[field].widget.attrs.update({'placeholder': 'Введите свой email'})
            elif field == 'first_name':
                self.fields[field].widget.attrs.update({'placeholder': 'Ваше имя'})
            elif field == 'password1':
                self.fields[field].widget.attrs.update({'placeholder': 'Придумайте свой пароль'})
            elif field == 'password2':
                self.fields[field].widget.attrs.update({'placeholder': 'Повторите придуманный пароль'})

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Старый пароль',
            'autocomplete': 'off',
        }),
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Новый пароль',
            'autocomplete': 'off',
        }),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите новый пароль',
            'autocomplete': 'off',
        }),
    )

class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите свой email',
            'autocomplete': 'off',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('Нет активного пользователя с таким email.')
        return email
    
class UserSetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Новый пароль',
            'autocomplete': 'off',
        }),
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите новый пароль',
            'autocomplete': 'off',
        }),
    )