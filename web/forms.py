from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

from web.models import User, Advert, Media


class BaseFormMixin:
    def __init__(self, *args, **kwargs):
        super(BaseFormMixin, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserLoginForm(BaseFormMixin, AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'Email-адреса'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ваш поточний пароль'}))


class SignUpForm(BaseFormMixin, UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=124, help_text='Required')
    phone_number = forms.IntegerField(help_text='Required')
    country = forms.CharField(max_length=50, help_text='Required')
    city = forms.CharField(max_length=50, help_text='Required')
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'country',
                  'city', 'avatar')


class AdvertForm(BaseFormMixin, forms.ModelForm):
    title = forms.CharField(max_length=70, required=True, help_text='Required')
    description = forms.CharField(max_length=9000, widget=forms.Textarea(attrs={'rows': 5}))
    category = forms.CharField(required=True)
    cost = forms.IntegerField()

    class Meta:
        model = Advert
        fields = ('title', 'description', 'category', 'cost')


class MediaForm(BaseFormMixin, forms.ModelForm):
    media = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Media
        fields = ('media',)