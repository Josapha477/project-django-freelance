from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('', views.contract_list, name='list'),
    path('<int:pk>/', views.contract_detail, name='detail'),
    path('<int:pk>/terminer/', views.complete_contract, name='complete'),
    path('<int:pk>/avis/', views.review_contract, name='review'),
]
