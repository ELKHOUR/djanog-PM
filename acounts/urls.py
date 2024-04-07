from django.contrib.auth.views import LoginView
from django.urls import path, include
from acounts.forms import UserLoginForm
from acounts.views import LogoutViewWithGet, RegisterView, edit_profile


urlpatterns=[
    path('login/', LoginView.as_view(authentication_form=UserLoginForm), name='login'),
        path('logout/', LogoutViewWithGet.as_view(), name='logout'),  # تمّ التعديل هنا 
        path('register/', RegisterView.as_view(), name='register'),
        path('profile/', edit_profile, name='profile'),
        path('', include('django.contrib.auth.urls'))
]