from django.urls import path

from users.views import login, logout, registration


app_name = 'users'


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
]