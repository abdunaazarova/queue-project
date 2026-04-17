from django.urls import path
from .views import UserLoginView, UserLogoutView, UserSignupView

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
