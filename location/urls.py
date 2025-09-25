from django.urls import path
from .views import *

urlpatterns = [
    path('state_list/', state_list, name='state_list'),
    path('create_state', create_state, name='create_state'),
    path('update_state/<int:pk>', update_state, name='update_state'),
    path('delete_state<int:pk>', delete_state, name='delete_state'),
    path('city_list', city_list, name='city_list'),
    path('create_city', create_city, name='create_city'),
    path('update_city/<int:pk>', update_city, name='update_city'),
    path('delete_city/<int:pk>', delete_city, name='delete_city'),

    # path('view_family/<int:pk>', view_family, name='view_family'),
]