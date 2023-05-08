from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .custom_decorators import auth_user_should_not_access
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import get_object_or_404

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from django.views import View
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings

from django.db.models import Q
from datetime import datetime, timedelta
from django.http import JsonResponse
import threading

from .models import CustomUser, Competition, Sport, Team, Event
from .forms import CustomUserCreationForm, CustomLoginForm, PasswordResetRequestForm, SetNewPasswordForm, CustomUserChangeForm, ContactForm, SportForm, TeamForm, CompetitionForm, CompetitionUpdateForm, EventForm


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


def get_events_and_competitions_this_week():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    events_this_week = Event.objects.filter(start_date_time__date__range=(start_of_week, end_of_week))
    competitions_this_week = Competition.objects.filter(start_date_time__date__range=(start_of_week, end_of_week))

    combined = list(events_this_week) + list(competitions_this_week)
    combined.sort(key=lambda x: x.start_date_time)

    return combined



# Dashboard (draft)
@login_required(login_url='login')
def dashboard(request):
    user = request.user

    # Get user's rating points
    rating_points = user.rating_points

    # Calculate the percentile
    total_users = CustomUser.objects.filter(is_superuser=False, is_staff=False).count()
    users_with_equal_or_less_rating = CustomUser.objects.filter(is_superuser=False, is_staff=False, rating_points__lte=user.rating_points).count()
    rating_percentile = (users_with_equal_or_less_rating / total_users) * 100

    # Get the total number of sports and their types
    single_player_sports = Sport.objects.filter(
        sport_type='Single-Player',
        competition__side_a=user.pk
    ).distinct() | Sport.objects.filter(
        sport_type='Single-Player',
        competition__side_b=user.pk
    ).distinct()
    team_player_sports = Sport.objects.filter(
        sport_type='Team-Player',
        competition__side_a__in=Team.objects.filter(members=user).values_list('pk', flat=True)
    ).distinct() | Sport.objects.filter(
        sport_type='Team-Player',
        competition__side_b__in=Team.objects.filter(members=user).values_list('pk', flat=True)
    ).distinct()

    
    single_player_count = single_player_sports.count()
    team_player_count = team_player_sports.count()
    sports_count = single_player_count + team_player_count
    

    # Get the user's teams count
    user_teams_count = user.team_set.count()

    # Get the current week's events and competitions
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    week_end = week_start + timedelta(days=6)

    events = Event.objects.filter(start_date_time__range=(week_start, week_end))
    competitions = Competition.objects.filter(start_date_time__range=(week_start, week_end))

    # Calculate the total number of events and competitions in the current week
    total_events_competitions = events.count() + competitions.count()

    # Calculate the difference in the number of events and competitions from last week
    last_week_start = week_start - timedelta(days=7)
    last_week_end = week_end - timedelta(days=7)

    last_week_events = Event.objects.filter(start_date_time__range=(last_week_start, last_week_end))
    last_week_competitions = Competition.objects.filter(start_date_time__range=(last_week_start, last_week_end))

    last_week_total_events_competitions = last_week_events.count() + last_week_competitions.count()
    
    events_competitions_difference = total_events_competitions - last_week_total_events_competitions
    
    user_teams = request.user.team_set.all()
    events_and_competitions_this_week = get_events_and_competitions_this_week()
    
    # User's single-player sports
    user_single_player_sports = Sport.objects.filter(
        sport_type='Single-Player',
        competition__side_a=user.pk
    ).distinct() | Sport.objects.filter(
        sport_type='Single-Player',
        competition__side_b=user.pk
    ).distinct()
    
    # User's team-player sports
    user_team_player_sports = Sport.objects.filter(
        sport_type='Team-Player',
        competition__side_a__in=user_teams
    ).distinct() | Sport.objects.filter(
        sport_type='Team-Player',
        competition__side_b__in=user_teams
    ).distinct()

    context = {
        'page': 'dashboard',
        'rating_points': rating_points,
        'rating_percentile': rating_percentile,
        'sports_count': sports_count,
        'single_player_count': single_player_count,
        'team_player_count': team_player_count,
        'user_teams_count': user_teams_count,
        'total_events_competitions': total_events_competitions,
        'events_competitions_difference': events_competitions_difference,
        'last_week_total_events_competitions': last_week_total_events_competitions,
        'user_teams': user_teams,
        'events_and_competitions_this_week': events_and_competitions_this_week,
        'user_single_player_sports': user_single_player_sports,
        'user_team_player_sports': user_team_player_sports,

    }
    return render(request, 'dashboard.html', context)



# analytics
@login_required(login_url='login')
def analytics(request):
    top_teams = Team.objects.all().order_by('-rating_points')
    top_players = CustomUser.objects.filter(is_superuser=False, is_staff=False).order_by('-rating_points')
    
    best_player = CustomUser.objects.filter(is_superuser=False, is_staff=False).order_by('-rating_points').first()
    best_team = Team.objects.order_by('-rating_points').first()
    
    # Get event counts
    total_events = Event.objects.count()
    interested_events_count = request.user.events_attended.count()
    declined_events_count = request.user.events_declined.count()
    
    context = {
        'page': 'analytics',
        'top_teams': top_teams,
        'top_players': top_players,
        'best_player': best_player,
        'best_team': best_team,
        'total_events': total_events,
        'interested_events_count': interested_events_count,
        'declined_events_count': declined_events_count,
        }
    
    return render(request, 'analytics.html', context)


# Event buttons
@login_required(login_url='login')
def event_action(request, event_id, action):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user

    if action == "interested":
        event.participants.add(user)
        event.declined_participants.remove(user)
    elif action == "decline":
        event.participants.remove(user)
        event.declined_participants.add(user)
    else:
        return JsonResponse({"error": "Invalid action"}, status=400)

    return redirect('profile')



# Profile
@login_required(login_url='login')
def profile(request):
    user = request.user
    user_form = CustomUserChangeForm(instance=user)
    contact_form = ContactForm(initial={'name': user.name, 'email': user.email})
    
    # Get user's rating points
    rating_points = user.rating_points
    
    # Get the user's teams count
    user_teams_count = user.team_set.count()
    
        # Get the total number of sports and their types
    single_player_sports = Sport.objects.filter(
        sport_type='Single-Player',
        competition__side_a=user.pk
    ).distinct() | Sport.objects.filter(
        sport_type='Single-Player',
        competition__side_b=user.pk
    ).distinct()
    team_player_sports = Sport.objects.filter(
        sport_type='Team-Player',
        competition__side_a__in=Team.objects.filter(members=user).values_list('pk', flat=True)
    ).distinct() | Sport.objects.filter(
        sport_type='Team-Player',
        competition__side_b__in=Team.objects.filter(members=user).values_list('pk', flat=True)
    ).distinct()

    
    single_player_count = single_player_sports.count()
    team_player_count = team_player_sports.count()
    sports_count = single_player_count + team_player_count
    
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get event counts
    total_events = Event.objects.count()
    interested_events_count = request.user.events_attended.count()
    
    events_this_week = Event.objects.filter(
    Q(start_date_time__date__range=(start_of_week, end_of_week)) | 
    Q(end_date_time__date__range=(start_of_week, end_of_week))
    )

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'user_form':
            user_form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Your changes have been applied.")
                return redirect('profile')
            else:
                messages.error(request, 'Something went wrong with the user form.')

        elif form_type == 'contact_form':
            contact_form = ContactForm(request.POST, initial={'name': user.name, 'email': user.email})
            if contact_form.is_valid():
                contact_form.save()
                
                email_subject = 'New Contact form submission at UCASports'
                email_body = render_to_string('_partials/contact_form_email.html', {
                    'name': contact_form.cleaned_data['name'],
                    'email': contact_form.cleaned_data['email'],
                    'subject': contact_form.cleaned_data['subject'],
                    'message': contact_form.cleaned_data['message'],
                    
                })

                email = EmailMessage(subject=email_subject, body=email_body,
                                    from_email=settings.CONTACT_EMAIL,
                                    to=settings.ADMIN_EMAIL
                                    )

                if not settings.TESTING:
                    EmailThread(email).start()
                
                
                messages.success(request, "Your message has been sent successfully.")
                return redirect('profile')
            else:
                messages.error(request, 'Something went wrong with the contact form.')

    context = {
        'page': 'profile', 
        'user_form': user_form, 
        'contact_form': contact_form, 
        'events_this_week': events_this_week,
        'rating_points': rating_points,
        'user_teams_count': user_teams_count,
        'sports_count': sports_count,
        'interested_events_count': interested_events_count,
        }
    return render(request, 'profile.html', context)



# Calendar
class CalendarView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        event_form = EventForm()
        events_api_url = reverse('api_events')
        competitions_api_url = reverse('api_competitions')
                
        context = {
            'event_form': event_form,
            'page': 'calendar',
            'events_api_url': events_api_url,
            'competitions_api_url': competitions_api_url,
        }
        return render(request, 'calendar.html', context)
    
    def post(self, request, *args, **kwargs):
        event_form = EventForm(request.POST)
        events_api_url = reverse('api_events')
        competitions_api_url = reverse('api_competitions')
        
        if 'add_event' in request.POST:
            if event_form.is_valid():
                event = event_form.save(commit=False)  # Save the form without committing to the database
                event.creator = request.user  # Set the creator to the current user
                event.save()  # Save the event to the database
                messages.success(request, 'New event added successfully.')
            else:
                messages.error(request, 'Something went wrong while adding new event.')

        context = {
            'event_form': event_form,
            'page': 'calendar',
            'events_api_url': events_api_url,
            'competitions_api_url': competitions_api_url,
        }
        return render(request, 'calendar.html', context)




# Points Distribution
def distribute_points(competition):
    side_a_score = competition.side_a_score
    side_b_score = competition.side_b_score

    if competition.sport.sport_type == 'Single-Player':
        user_a = CustomUser.objects.get(id=int(competition.side_a))
        user_b = CustomUser.objects.get(id=int(competition.side_b))

        user_a.rating_points += 2
        user_b.rating_points += 2

        if side_a_score > side_b_score:
            user_a.rating_points += 4
            user_a.wins += 1
            user_b.losses += 1
        elif side_a_score < side_b_score:
            user_b.rating_points += 4
            user_b.wins += 1
            user_a.losses += 1

        user_a.save()
        user_b.save()

    elif competition.sport.sport_type == 'Team-Player':
        team_a = Team.objects.get(id=int(competition.side_a))
        team_b = Team.objects.get(id=int(competition.side_b))

        team_a.rating_points += 2
        team_b.rating_points += 2

        if side_a_score > side_b_score:
            team_a.rating_points += 4
            team_a.wins += 1
            team_b.losses += 1

            for user in team_a.members.all():
                user.rating_points += 3
                user.save()
            for user in team_b.members.all():
                user.rating_points += 1
                user.save()

        elif side_a_score < side_b_score:
            team_b.rating_points += 4
            team_b.wins += 1
            team_a.losses += 1

            for user in team_b.members.all():
                user.rating_points += 3
                user.save()
            for user in team_a.members.all():
                user.rating_points += 1
                user.save()

        team_a.save()
        team_b.save()





# Site Manager
class SiteManagerView(LoginRequiredMixin, View):
    login_url = 'login'  # Redirect to the login page if the user is not logged in
    def get(self, request, *args, **kwargs):
        sport_form = SportForm()
        team_form = TeamForm()
        competition_form = CompetitionForm(*args)
        competition_update_form = CompetitionUpdateForm()
        api_url = reverse('api_competitors')
        
        users_competitions = Competition.objects.filter(sport__sport_type='Single-Player').order_by('-start_date_time')
        teams_competitions = Competition.objects.filter(sport__sport_type='Team-Player').order_by('-start_date_time')
        
        sports = Sport.objects.all()
        sports_with_team_count = []
        for sport in sports:
            teams_count = Team.objects.filter(sport=sport).count()
            sports_with_team_count.append({
                'sport': sport,
                'teams_count': teams_count
            })
        
        
        teams = Team.objects.all()
        teams_with_player_count = []
        for team in teams:
            players_count = team.members.count()
            teams_with_player_count.append({
                'team': team,
                'players_count': players_count
            })
            
        
        context = {
            'sport_form': sport_form,
            'team_form': team_form,
            'competition_form': competition_form,
            'competition_update_form': competition_update_form, 
            'page': 'site_manager',
            'api_url': api_url,
            
            'users_competitions': users_competitions,
            'teams_competitions': teams_competitions,
            'sports_with_team_count': sports_with_team_count,
            'teams_with_player_count': teams_with_player_count,
        }
        return render(request, 'site_manager.html', context)

    def post(self, request, *args, **kwargs):
        sport_form = SportForm(request.POST)
        team_form = TeamForm(request.POST)
        competition_form = CompetitionForm(request.POST, *args)  # Pass *args here
        competition_update_form = CompetitionUpdateForm(request.POST)
        api_url = reverse('api_competitors')
        
        users_competitions = Competition.objects.filter(sport__sport_type='Single-Player').order_by('-start_date_time')
        teams_competitions = Competition.objects.filter(sport__sport_type='Team-Player').order_by('-start_date_time')
        
        sports = Sport.objects.all()
        sports_with_team_count = []
        for sport in sports:
            teams_count = Team.objects.filter(sport=sport).count()
            sports_with_team_count.append({
                'sport': sport,
                'teams_count': teams_count
            })
        
        
        teams = Team.objects.all()
        teams_with_player_count = []
        for team in teams:
            players_count = team.members.count()
            teams_with_player_count.append({
                'team': team,
                'players_count': players_count
            })
        
        if 'add_sport' in request.POST:
            if sport_form.is_valid():
                sport_form.save()
                messages.success(request, 'New sport added successfully.')
            else:
                messages.error(request, 'Something went wrong while adding new sport.')

        elif 'add_team' in request.POST:
            if team_form.is_valid():
                team_form.save()
                messages.success(request, 'New team added successfully.')
            else:
                messages.error(request, 'Something went wrong while adding new team.')

        elif 'add_competition' in request.POST:
            if competition_form.is_valid():
                competition_form.save()
                messages.success(request, 'New competition added successfully.')
            else:
                messages.error(request, 'Something went wrong while adding new competition.')

        elif 'update_competition' in request.POST:
            competition_id = request.POST.get('competition_id')  # Get the competition_id from the submitted form data
            competition = Competition.objects.get(pk=competition_id)  # Get the competition object using the competition_id
            if competition_update_form.is_valid():
                competition.side_a_score = competition_update_form.cleaned_data['side_a_score']
                competition.side_b_score = competition_update_form.cleaned_data['side_b_score']
                competition.status = competition_update_form.cleaned_data['status']
                
                if competition.status == "Finished":
                    distribute_points(competition)
                
                competition.save()
                messages.success(request, 'Competition updated successfully.')
            else:
                messages.error(request, 'Something went wrong while updating the competition.')

        context = {
            'sport_form': sport_form,
            'team_form': team_form,
            'competition_form': competition_form,
            'competition_update_form': competition_update_form,  # Add this line
            'page': 'site_manager',
            'api_url': api_url,
            
            'users_competitions': users_competitions,
            'teams_competitions': teams_competitions,
            'sports_with_team_count': sports_with_team_count,
            'teams_with_player_count': teams_with_player_count,
        }
        return render(request, 'site_manager.html', context)



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