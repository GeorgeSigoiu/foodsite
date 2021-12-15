from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name="profiles"),
    path('create-user', views.createUser, name="create-user"),
    path('login-user', views.loginUser, name="login-user"),
    path('logout-user', views.logoutUser, name="logout-user"),
    path('user-profile/<str:username>', views.showProfile, name="user-profile"),
    path('update-user/', views.updatePersonalInfo, name="update-user"),
    path('create-bill/<str:bill_number>', views.createBill, name="create-bill"),
]
