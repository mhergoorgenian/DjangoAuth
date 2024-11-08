from django.urls import path
from .views import UsersView,LoginView,RegisterView,MeView,UserView
urlpatterns = [
    
    path('users',UsersView.as_view(),name="get_users"),
    path('user/<int:id>',UserView.as_view(),name="get_user"),
    path('me',MeView.as_view(),name="get_mydata"),
    path('login', LoginView.as_view(),name="login_user"),
    path('register', RegisterView.as_view(),name="register_user")

]
