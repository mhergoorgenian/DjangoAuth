from django.urls import path
from .views import UserProfileView,UserLoginView,UserRegisterView
urlpatterns = [
    path('users',UserProfileView.as_view(),name="get users"),
    path('login', UserLoginView.as_view(),name="login user"),
    path('register', UserRegisterView.as_view(),name="register user")
]
