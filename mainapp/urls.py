from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('get_all_coordinates/', views.get_all_coordinates, name='get_all_coordinates'),


    path('election_index/', views.election_index, name='election_index'),
    path('election_visualize/', views.election_visualize, name='election_visualize'),
    path('election_visualize/<int:caseid>', views.election_visualize, name='election_visualize'),
    # path('callback/', views.callback, name='callback'),
]