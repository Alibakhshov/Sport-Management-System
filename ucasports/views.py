from django.shortcuts import render, redirect
from django.contrib import messages
from .custom_decorators import auth_user_should_not_access
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomLoginForm, PasswordResetRequestForm, SetNewPasswordForm, CustomUserChangeForm


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()
        

def send_activation_email(user, request):
    token = generate_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = request.build_absolute_uri(reverse('activate_user', args=[uid, token]))
    
    email_subject = 'Activate your account'
    email_body = render_to_string('_partials/activate.html', {
        'user': user,
        'verification_link': verification_link
        
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.CONTACT_EMAIL,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()


# Homepage
def home(request):
    return render(request, 'home.html')


# Dashboard (draft)
def dashboard(request):
    context = {'page': 'dashboard'}
    return render(request, 'dashboard.html', context)


# Login
@auth_user_should_not_access
def loginPage(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user:
                if not user.is_active:
                    messages.add_message(request, messages.ERROR,
                                         'Email is not verified, please check your email inbox')
                    return render(request, 'login_register.html', {'form': form, 'page': 'login'}, status=401)

                login(request, user)
                return redirect(reverse('dashboard'))
            else:
                messages.add_message(request, messages.ERROR,
                                     'Invalid credentials, try again')
                return render(request, 'login_register.html', {'form': form, 'page': 'login'}, status=401)

        else:
            print("Form is not valid")  # Debugging
            print(form.errors)  # Show form errors

    form = CustomLoginForm()
    context = {'form': form, 'page': 'login'}
    return render(request, 'login_register.html', context)
# def loginPage(request):
#     if request.method == 'POST':
#         form = CustomLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             user = authenticate(request, email=email, password=password)

#             if user and not user.is_email_verified:
#                 messages.add_message(request, messages.ERROR,
#                                      'Email is not verified, please check your email inbox')
#                 return render(request, 'login_register.html', {'form': form, 'page': 'login'}, status=401)

#             if not user:
#                 messages.add_message(request, messages.ERROR,
#                                      'Invalid credentials, try again')
#                 return render(request, 'login_register.html', {'form': form, 'page': 'login'}, status=401)

#             login(request, user)
#             return redirect(reverse('home'))

#     form = CustomLoginForm()
#     context = {'form': form, 'page': 'login'}
#     return render(request, 'login_register.html', context)


# Logout
def logoutUser(request):
    logout(request)

    messages.add_message(request, messages.SUCCESS,'Successfully logged out')
    return redirect(reverse('login'))


# Register
@auth_user_should_not_access
def registerPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the user instance without committing it to the database
            user.save()  # Save the user instance to the database after sending the email
            send_activation_email(user, request)  # Send the activation email
            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account')

            # Redirect to a success page or the login page
            return redirect('login')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, error)
            return render(request, 'login_register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'login_register.html', {'form': form})
    
    

# Password reset request view
@auth_user_should_not_access
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                messages.add_message(request, messages.ERROR,
                                         'User with this email does not exist.')
                user = None
                
            if user is not None:
                token = generate_token.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[uid, token]))
                
                email_subject = 'Reset your password'
                email_body = render_to_string('_partials/password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link
                })
                
                email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.CONTACT_EMAIL,
                         to=[user.email]
                         )

                if not settings.TESTING:
                    EmailThread(email).start()

                messages.success(request, 'We sent you an email with instructions to reset your password.')
                return redirect('login')

    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'password_reset_request.html', {'form': form})



# Password reset confirmation view
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, 'Your password has been changed successfully. Please log in with your new password.')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match. Please try again.')
        else:
            form = SetNewPasswordForm()

        return render(request, 'password_reset_form.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('password_reset_request')
    
    
    

# Activate User
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

    #except Exception as e:
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))
    return render(request, 'activation_failed.html', {"user": user})