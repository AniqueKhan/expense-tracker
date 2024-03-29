from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from authentication.utils import token_generator
# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({"username_error": "Username should only contain alphanumeric characters"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "User with this username already exists"}, status=400)
        return JsonResponse({"username_valid": True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({"email_error": "Invalid Email"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "User with this email already exists"}, status=400)
        return JsonResponse({"email_valid": True})


class SignupView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {
            "fieldValues": request.POST
        }

        if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages.error(
                    request, "Password must be atleast 6 characters")
                return render(request, 'authentication/signup.html', context)

            user = User.objects.create_user(email=email, username=username)
            user.set_password(password)
            user.is_active = False

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs={"uidb64":uidb64,"token":token_generator.make_token(user)})
            activate_url = f'http://{domain}{link}'

            # Email
            email_subject = "Account Activation Email"
            email_body = f"Hi, {user.username}. Please use this link to verify your account.\n{activate_url}"
            email = EmailMessage(
                email_subject, email_body, 'noreply@semicolon.com', [email],
            )
            email.send(fail_silently=False)

            user.save()
            messages.success(request, "Account created successfully")
            return render(request, 'authentication/signup.html')

        return render(request, 'authentication/signup.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('index')
