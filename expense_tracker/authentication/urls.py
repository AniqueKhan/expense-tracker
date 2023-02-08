from django.urls import path
from authentication.views import *
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path("signup", SignupView.as_view(), name='signup'),
    path("validate_username", csrf_exempt(UsernameValidationView.as_view()),
         name='validate-username'),
    path("validate_email", csrf_exempt(EmailValidationView.as_view()),
         name='validate-email'),
]
