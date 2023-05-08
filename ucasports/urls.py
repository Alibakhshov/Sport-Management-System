from django.urls import path
from . import views
from .views import SiteManagerView, CalendarView

appname = "ucasports"

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    
    path('dashboard/', views.dashboard, name="dashboard"),
    path('analytics/', views.analytics, name="analytics"),
    path('profile/', views.profile, name="profile"),
    
    path('event/<int:event_id>/<str:action>/', views.event_action, name='event_action'),
    
    path('calendar/', CalendarView.as_view(), name="calendar"),
    path('site-manager/', SiteManagerView.as_view(), name="site_manager"),
 
    path('activation/<str:uidb64>/<str:token>/', views.activate_user, name='activate_user'),
    
    path('password-reset/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    path('reset/', views.password_reset_request, name='password_reset_request'),
    
    path('', views.home, name="home"),
    
]