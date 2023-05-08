from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput, EmailInput
from .models import CustomUser, Contact, Team, Sport, Event, Competition
from django.forms import ModelMultipleChoiceField, ModelChoiceField
from django.urls import reverse

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
        fields = ['name', 'username', 'bio', 'avatar']
        
        
        
class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", 'readonly': 'readonly'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control", 'readonly': 'readonly'}))
    
    subject = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Subject"}
    ))
    
    message = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control", "rows": 4}
    ))
    
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
    #     attrs={
    #         'data-theme': 'dark',
    #     }
    # ))
    
    
    class Meta:
        model = Contact
        fields = '__all__'
        

class CustomUserChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.email})"
    
    
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'avatar', 'sport', 'members']
        widgets = {
            'members': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['sport'].queryset = Sport.objects.filter(sport_type='Team-Player')
        self.fields['sport'].empty_label = None
        self.fields['sport'].required = True
        self.fields['members'] = CustomUserChoiceField(queryset=CustomUser.objects.filter(is_superuser=False, is_staff=False), widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
        

class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name', 'sport_type']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'sport',
            'start_date_time',
            'end_date_time',
            'location',
            'description',
        ]
        widgets = {
            'start_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'startDate'}),
            'end_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'id': 'endDate'}),
        }
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['sport'].empty_label = None

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            'name',
            'sport',
            'start_date_time',
            'end_date_time',
            'location',
            'description',
            'side_a',
            'side_b',
        ]
        widgets = {
            'sport': forms.Select(attrs={'id': 'sport_name'}),
            'side_a': forms.Select(attrs={'class': 'form-select competitor'}),
            'side_b': forms.Select(attrs={'class': 'form select competitor'}),
            'start_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}), 
        }
        
    def __init__(self, *args, **kwargs):
        super(CompetitionForm, self).__init__(*args, **kwargs)
        self.fields['sport'].empty_label = None
        
        api_url = reverse('api_competitors')  # Generate the URL
        self.fields['sport'].widget.attrs.update({'data-api-url': api_url})  # Set the data-api-url attribute


class CompetitionUpdateForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['side_a_score', 'side_b_score', 'status']

