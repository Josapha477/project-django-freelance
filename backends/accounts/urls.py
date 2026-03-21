from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('inscription/', views.register, name='register'),
    path('connexion/', views.CustomLoginView.as_view(), name='login'),
    path('deconnexion/', views.CustomLogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    
    path('profil/', views.profile, name='profile'),
    path('profil/freelancer/completer/', views.complete_freelancer_profile, name='complete_freelancer_profile'),
]
