from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView

from train_reg.models import TrainRegModel
from .forms import UserRegisterForm, UserLoginForm, ImageDownload
from django.urls import reverse_lazy
from django.views import View

from .models import Image


# Create your views here.
class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'auth_user/registration.html'
    success_url = reverse_lazy('main')


class LoginUser(LoginView):
    form_class = UserLoginForm  # AuthenticationForm
    template_name = 'auth_user/login_user.html'
    success_url = reverse_lazy('main')


def logout_fun(request):
    logout(request)
    return redirect('log')


def account(request):
    if request.user.is_authenticated:
        # получение из базы данных тренировок
        trains = TrainRegModel.objects.filter(client__id=request.user.id, is_booked=True)
        if len(trains) == 0:
            trains = None
        try:
            photo = Image.objects.get(id=request.user.id).image.url
        except:
            photo = Image.objects.get(id=1).image.url

        return render(request, 'auth_user/my_personal_acc.html', context={'photo': photo, 'trains': trains, })
    else:
        return HttpResponseNotFound('<h2> Вы не вошли в аккаунт! </h2>')


# class EditImage(CreateView):
#    form_class = ImageDownload
#    template_name = 'auth_user/image_persacc.html'
#    success_url = reverse_lazy('main')

class EditImage(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseNotFound('<h2> Вы не зарегистрированы! </h2>')
        form = ImageDownload()
        return render(request, 'auth_user/image_persacc.html', context={'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseNotFound('<h2> Вы не зарегистрированы! </h2>')
        # если пользователь зарегестрирован то
        form = ImageDownload(request.POST, request.FILES)
        if form.is_valid():
            new_photo = Image(image=form.cleaned_data['image'], id=request.user.id)
            new_photo.save()
            return redirect('my_account')
        return render(request, 'auth_user/image_persacc.html', context={'form': form})
