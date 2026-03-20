from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('nouveau/', views.project_create, name='create'),
    path('<int:pk>/', views.project_detail, name='detail'),
    path('<int:pk>/modifier/', views.project_edit, name='edit'),
    path('<int:pk>/proposer/', views.submit_proposal, name='submit_proposal'),
    path('<int:project_pk>/proposition/<int:proposal_pk>/accepter/', views.accept_proposal, name='accept_proposal'),
]
