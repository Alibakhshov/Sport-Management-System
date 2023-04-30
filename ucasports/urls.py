from django.urls import path
from . import views

appname = "ucasports"

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    
    # path('about/', views.about, name="about"),
    # path('faq/', views.faq, name="faq"),
    # path('contact/', views.contact, name="contact"),
    
    path('dashboard/', views.dashboard, name="dashboard"),
    path('calendar/', views.calendar, name="calendar"),
    # path('settings/', views.settings_page, name="settings"),
    path('activation/<str:uidb64>/<str:token>/', views.activate_user, name='activate_user'),
    
    path('password-reset/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # path('activate/<uidb64>/<token>', views.activate_user, name='activate'),
    
    path('reset/', views.password_reset_request, name='password_reset_request'),
    
    path('', views.home, name="home"),
    
]