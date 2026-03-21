from django.urls import path
from . import views

app_name = 'freelancers'

urlpatterns = [
    path('', views.freelancer_list, name='list'),
    path('<int:pk>/', views.freelancer_detail, name='detail'),
]
