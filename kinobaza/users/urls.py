from django.urls import path

from users.views import login, logout, UserRegistrationView


app_name = 'users'


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
]
