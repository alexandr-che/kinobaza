from django.contrib import auth, messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse

from users.forms import UserLoginForm


# class UserLogin(SuccessMessageMixin, LoginView):
#     template_name = 'users/login.html'
#     form_class = UserLoginForm
#     success_url = reverse_lazy('movies:movie_list')
#     success_message = 'Добро пожаловать, %(username)s!'

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            message = messages.success(request, f'Добро пожаловать {user.username}!')
            return redirect(reverse('movies:movie_list'))
        else:
            messages.error(
                request, 'Ошибка авторизации. Пожалуйста, проверьте ваше имя пользователя и пароль.'
                )
            return redirect(reverse('movies:movie_list'))


def logout(request):
    auth.logout(request)
    return redirect(reverse('movies:movie_list'))


def registration():
    ...