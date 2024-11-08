from django.urls import path
from .views import UserProfileView,UserLoginView,UserRegisterView
urlpatterns = [
    path('users',UserProfileView.as_view(),name="get_users"),
    path('users/<int:id>', UserProfileView.as_view(), name="get_users"),
    path('login', UserLoginView.as_view(),name="login_user"),
    path('register', UserRegisterView.as_view(),name="register_user")
]
