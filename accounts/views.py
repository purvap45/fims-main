from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
import re

def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if not CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"field": 'email', "success": False, "errorMessage": "Email not registered."})

        user = authenticate(request, email = email, password = password)

        if user is None:
            return JsonResponse({"field": 'password', "success": False, "errorMessage": "Invalid Password."})
        else:
            login(request, user)
            return JsonResponse({"success": True})

    return render(request, 'login.html')

@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        
        try:
            user = CustomUser.objects.get(email=email)
            #create new PasswordReset
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset_password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )
            email_message.fail_silently = True
            email_message.send()
            return redirect('password_reset_sent', reset_id=new_password_reset.reset_id)

        except CustomUser.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found.")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')

def password_reset_sent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # messages.error(request, 'Invalid reset id')
        return redirect('forgot_password')

def reset_password(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)
        expiration_time = password_reset_id.created_at + timezone.timedelta(minutes=10)
        # print(expiration_time)
        # print(timezone.now())
        if timezone.now() > expiration_time:
            passwords_have_error = True
            # messages.error(request, 'Reset link has expired')
            password_reset_id.delete()
            return redirect('link_expired')

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False
            pass_regex = r'(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'

            if not password:
                passwords_have_error = True
                messages.error(request, "Password is required.")

            if not confirm_password:
                passwords_have_error = True
                messages.error(request, "Confirm Password is required.")

            elif not re.match(pass_regex, password):
                passwords_have_error = True
                messages.error(request, "Password must have 8+ chars, 1 Uppercase, 1 Number, 1 Special Char.")

            elif password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')
                
            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()
                password_reset_id.delete()
                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login_page')
            else:
                return redirect('reset_password', reset_id=reset_id)

    except PasswordReset.DoesNotExist:
        # messages.error(request, 'Invalid reset id')
        return redirect('link_expired')

    return render(request, 'reset_password.html')

def link_expired(request):
    return render(request, 'link_expired.html')
    