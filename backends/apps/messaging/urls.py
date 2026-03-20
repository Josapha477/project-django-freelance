from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='list'),
    path('<int:pk>/', views.conversation_detail, name='detail'),
    path('nouveau/<int:user_pk>/', views.start_conversation, name='start'),
]
