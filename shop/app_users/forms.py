from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

User = get_user_model()


class UserCreateForm(UserCreationForm):
    image_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'gif'],
        message='File extension not allowed. Allowed extensions include  .png'
    )

    def validate_image_size(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    password1 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                                 'data-validate': 'requirePassword',
                                                                                                 'placeholder': 'Введите пароль',
                                                                                                 'autocomplete': 'new-password'}))
    password2 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                                 'data-validate': 'requireRepeatPassword',
                                                                                                 'placeholder': 'Введите пароль повторно',
                                                                                                 'autocomplete': 'new-password'}))
    full_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                                             'data-validate': 'require',
                                                                                             'placeholder': 'Введите ФИО'}))
    email = forms.EmailField(label='e-mail', required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                                          'data-validate': 'requireMail',
                                                                                          'maxlength': '150'}))
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
    image_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'gif'],
        message='File extension not allowed. Allowed extensions include  .png'
    )

    def validate_image_size(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    password1 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                                 'data-validate': 'requirePassword',
                                                                                                 'placeholder': 'Введите пароль',
                                                                                                 'autocomplete': 'new-password'}))
    password2 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                                                 'data-validate': 'requireRepeatPassword',
                                                                                                 'placeholder': 'Введите пароль повторно',
                                                                                                 'autocomplete': 'new-password'}))
    full_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                                             'data-validate': 'require',
                                                                                             'placeholder': 'Введите ФИО'}))
    email = forms.EmailField(label='e-mail', required=True, widget=forms.TextInput(attrs={'class': 'form-input',
                                                                                          'data-validate': 'require',
                                                                                          'maxlength': '150'}))
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


# validators=[image_validator, validate_image_size],
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(required=True, label='Email', widget=forms.TextInput(attrs={'class': 'form-input',
                                                                                            'data-validate': 'require',
                                                                                            'maxlength': '150',
                                                                                            'placeholder': 'Введите e-mail',
                                                                                            'autocomplete': 'email'}))

    password = forms.CharField(max_length=150, label='Пароль', required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-input',
                                                                 'data-validate': 'require',
                                                                 'placeholder': 'Введите пароль',
                                                                 'autocomplete': 'password'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
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
                                          "autocomplete": "new-password"}),
        strip=False
    )
    new_password2 = forms.CharField(
        max_length=150,
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input',
                                          'data-validate': 'requireRepeatPassword',
                                          'placeholder': 'Введите пароль повторно',
                                          "autocomplete": "new-password"}),
    )
