from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
import re, logging

from .models import CustomUser, PasswordReset

logger = logging.getLogger(__name__)

def login_page(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email or not password:
                return JsonResponse({"success": False, "errorMessage": "Email and password are required."})

            if not CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"field": 'email', "success": False, "errorMessage": "Email not registered."})

            user = authenticate(request, email=email, password=password)

            if user is None:
                return JsonResponse({"field": 'password', "success": False, "errorMessage": "Invalid Password."})
            else:
                login(request, user)
                return JsonResponse({"success": True})

        return render(request, 'login.html')

    except Exception as e:
        logger.exception("Error in login_page: %s", e)
        return JsonResponse({"success": False, "errorMessage": "An unexpected error occurred. Please try again."})


@login_required
def logout_page(request):
    try:
        logout(request)
        return redirect('login_page')
    except Exception as e:
        logger.exception("Error in logout_page: %s", e)
        messages.error(request, "Something went wrong while logging out.")
        return redirect('login_page')


def forgot_password(request):
    try:
        if request.method == "POST":
            email = request.POST.get('email')

            if not email:
                return JsonResponse({"field": 'email', "success": False, "errorMessage": "Email is required."})

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return JsonResponse({"field": 'email', "success": False, "errorMessage": f"No user with email '{email}' found."})

            # Create new PasswordReset
            new_password_reset = PasswordReset.objects.create(user=user)

            password_reset_url = reverse('reset_password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
            email_body = f'Reset your password using the link below:\n\n{full_password_reset_url}'

            try:
                email_message = EmailMessage(
                    'Reset your password',
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                email_message.fail_silently = True
                email_message.send()
            except Exception as mail_error:
                logger.warning("Email sending failed: %s", mail_error)

            redirectURL = reverse('password_reset_sent', kwargs={'reset_id': new_password_reset.reset_id})
            return JsonResponse({"success": True, "redirectURL": redirectURL})

        return render(request, 'forgot_password.html')

    except Exception as e:
        logger.exception("Error in forgot_password: %s", e)
        return JsonResponse({"success": False, "errorMessage": "An unexpected error occurred. Please try again later."})


def password_reset_sent(request, reset_id):
    try:
        if PasswordReset.objects.filter(reset_id=reset_id).exists():
            return render(request, 'password_reset_sent.html')
        else:
            return redirect('forgot_password')
    except Exception as e:
        logger.exception("Error in password_reset_sent: %s", e)
        return redirect('forgot_password')


def reset_password(request, reset_id):
    try:
        password_reset = PasswordReset.objects.get(reset_id=reset_id)
        expiration_time = password_reset.created_at + timezone.timedelta(minutes=10)

        if timezone.now() > expiration_time:
            password_reset.delete()
            return redirect('link_expired')

        if request.method == "POST":
            try:
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')

                pass_regex = r'(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'

                if not password:
                    return JsonResponse({"field": 'password', "success": False, "errorMessage": "Password is required."})
                if not confirm_password:
                    return JsonResponse({"field": 'confirm_password', "success": False, "errorMessage": "Confirm Password is required."})
                if not re.match(pass_regex, password):
                    return JsonResponse({"field": 'password', "success": False, "errorMessage": "Password must have 8+ chars, 1 Uppercase, 1 Number, 1 Special Char."})
                if password != confirm_password:
                    return JsonResponse({"field": 'confirm_password', "success": False, "errorMessage": "Passwords do not match."})

                user = password_reset.user
                user.set_password(password)
                user.save()
                password_reset.delete()

                return JsonResponse({"success": True, "message": "Password reset successful. Proceed to login."})

            except Exception as inner_error:
                logger.exception("Error while resetting password: %s", inner_error)
                return JsonResponse({"success": False, "errorMessage": "An unexpected error occurred. Please try again."})

        context = {"reset_id": reset_id}
        return render(request, 'reset_password.html', context)

    except PasswordReset.DoesNotExist:
        return redirect('link_expired')
    except Exception as e:
        logger.exception("Error in reset_password: %s", e)
        return redirect('link_expired')


def link_expired(request):
    try:
        return render(request, 'link_expired.html')
    except Exception as e:
        logger.exception("Error in link_expired view: %s", e)
        messages.error(request, "An error occurred.")
        return redirect('forgot_password')
