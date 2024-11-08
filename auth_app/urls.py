from django.urls import path
from .views import UserProfileView,UserLoginView,UserRegisterView
urlpatterns = [
    path('users',UserProfileView.as_view(),name="get_users"),
    path('me',UserProfileView.as_view(),name="get_mydata"),
    path('login', UserLoginView.as_view(),name="login_user"),
    path('register', UserRegisterView.as_view(),name="register_user")
]
