from django.contrib import admin
from django.urls import path, include
from .views import RegisterUser, LoginUser, logout_fun, account, EditImage

urlpatterns = [
    path('login/', LoginUser.as_view(), name='log'),
    path('logout/', logout_fun, name='logout'),
    path('register/', RegisterUser.as_view(), name='reg'),
    path('my_account/', account, name='my_account'),
    path('editphoto/', EditImage.as_view(), name='edit_photo'),
    # path('account/', include('auth_user.urls'), name='account'),
]
