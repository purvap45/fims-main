from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('logout_page/', logout_page, name='logout_page'),
    
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('password_reset_sent/<str:reset_id>/', password_reset_sent, name='password_reset_sent'),
    path('reset_password/<str:reset_id>/', reset_password, name='reset_password'),
    path('link_expired/', link_expired, name='link_expired'),
]
