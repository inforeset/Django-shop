from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                                 'data-validate': 'requirePassword',
                                                                                                 'placeholder': 'Введите пароль',
                                                                                                 'autocomplete': 'new-password',
                                                                                                 'maxlength': '150'}))
    password2 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                                 'data-validate': 'requireRepeatPassword',
                                                                                                 'placeholder': 'Введите пароль повторно',
                                                                                                 'autocomplete': 'new-password',
                                                                                                 'maxlength': '150'}))
    full_name = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                                             'data-validate': 'require',
                                                                                             'placeholder': 'Введите ФИО',
                                                                                             'maxlength': '254'}))
    email = forms.EmailField(max_length=254, label='e-mail', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-input',
                                                           'data-validate': 'requireMail',
                                                           'maxlength': '254'}))
    phoneNumber = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                               'data-validate': 'requirePhone'}))
    avatar = forms.ImageField(required=False,
                              widget=forms.ClearableFileInput(attrs={'class': 'Profile-file form-input',
                                                                     'type': "file",
                                                                     'accept': ".jpg,.gif,.png",
                                                                     'data-validate': "onlyImgAvatar"
                                                                     }))

    class Meta:
        model = User
        fields = ('password1', 'password2', 'full_name', 'email', 'phoneNumber', 'avatar')


class MyUserChangeForm(UserChangeForm):
    password1 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                                 'data-validate': 'requirePassword',
                                                                                                 'placeholder': 'Введите пароль',
                                                                                                 'autocomplete': 'new-password',
                                                                                                 'maxlength': '150'}))
    password2 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                                 'data-validate': 'requireRepeatPassword',
                                                                                                 'placeholder': 'Введите пароль повторно',
                                                                                                 'autocomplete': 'new-password',
                                                                                                 'maxlength': '150'}))
    full_name = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                                             'data-validate': 'require',
                                                                                             'placeholder': 'Введите ФИО',
                                                                                             'maxlength': '254'}))
    email = forms.EmailField(max_length=254, label='e-mail', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-input',
                                                           'data-validate': 'require',
                                                           'maxlength': '254'}))
    phoneNumber = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                               'data-validate': 'require'}))
    avatar = forms.ImageField(required=False,
                              widget=forms.FileInput(attrs={'class': 'Profile-file form-input',
                                                            'type': "file",
                                                            'accept': ".jpg,.gif,.png",
                                                            'data-validate': "onlyImgAvatar"
                                                            }))

    class Meta:
        model = User
        fields = ('password1', 'password2', 'full_name', 'email', 'phoneNumber', 'avatar')


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, required=True, label='Email',
                                widget=forms.TextInput(attrs={'class': 'form-input',
                                                              'data-validate': 'require',
                                                              'maxlength': '254',
                                                              'placeholder': 'Введите e-mail',
                                                              'autocomplete': 'email'}))

    password = forms.CharField(max_length=150, label='Пароль', required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                 'data-validate': 'require',
                                                                 'placeholder': 'Введите пароль',
                                                                 'autocomplete': 'password',
                                                                 'maxlength': '150'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254,
                             required=True,
                             widget=forms.TextInput(attrs={'class': 'form-input',
                                                           'data-validate': 'require',
                                                           'maxlength': '254',
                                                           'autocomplete': 'email'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-input',
                                          'data-validate': 'requirePassword',
                                          'placeholder': 'Введите пароль',
                                          "autocomplete": "new-password",
                                          'maxlength': '150'}),
        strip=False
    )
    new_password2 = forms.CharField(
        max_length=150,
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input',
                                          'data-validate': 'requireRepeatPassword',
                                          'placeholder': 'Введите пароль повторно',
                                          "autocomplete": "new-password",
                                          'maxlength': '150'}),
    )
