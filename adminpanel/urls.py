from django.urls import path, include
from .apis import *

urlpatterns = [
    path('register_user/', register_user),
    path('login_user/', login_user),
    path('get_user/', get_user),
]
