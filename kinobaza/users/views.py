from django.views.generic import CreateView
from django.contrib import auth, messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from users.forms import UserRegistrationForm
from users.models import User


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, f'Добро пожаловать {user.username}!')
            return redirect(reverse('movies:movie_list'))
        else:
            messages.error(
                request, 'Ошибка авторизации. Пожалуйста, проверьте ваше имя пользователя и пароль.'
                )
            return redirect(reverse('movies:movie_list'))


def logout(request):
    auth.logout(request)
    return redirect(reverse('movies:movie_list'))


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_message = 'Вы успешно зарегистрировались и вошли в аккаунт'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(self.request, user)
                return redirect(reverse('movies:movie_list'))
        else:
            self.form_invalid(form)