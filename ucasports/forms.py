from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput, EmailInput, PasswordInput
from .models import CustomUser

email_validator = RegexValidator(
    r'^[a-zA-Z0-9._%+-]+@ucentralasia\.org$',
    message="Only @ucentralasia.org email addresses are allowed."
)


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))

    class Meta:
        model = CustomUser
        fields = ('name', 'username', 'email')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g John Doe'}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'customusername'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@ucentralasia.org'}),
        }
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise ValidationError('Name field cannot be empty. Please enter your name.')
        return name
    

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Username is already taken. Please choose a different one.')
        if len(username) < 5:
            raise ValidationError('Username should be at least 5 characters long.')
        
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email is already in use. Please choose a different one.')
        email_validator(email)
        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match. Please try again.')

        if len(password1) < 8:
            raise ValidationError('Password should be at least 8 characters long.')

        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user
    # email = forms.EmailField(required=True, validators=[email_validator])

    # class Meta:
    #     model = CustomUser
    #     fields = ['name', 'username', 'email', 'password1', 'password2']

class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@ucentralasia.org'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'})
    )


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@ucentralasia.org'})
        )


class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))

    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'email', 'bio', 'avatar']