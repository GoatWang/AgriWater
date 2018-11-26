from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('election_index/', views.election_index, name='election_index'),
    # path('callback/', views.callback, name='callback'),
]