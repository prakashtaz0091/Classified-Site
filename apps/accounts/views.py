import requests
from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import RegistrationForm, UserProfileForm
from .models import Account, UserProfile


def Login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            # url = request.META.get('HTTP_REFERER')
            # try:
            #     query = requests.utils.urlparse(url).query

            #     params = dict(x.split('=') for x in query.split('&'))
            #     if 'next' in params:
            #         nextPage = params['next']
            #         return redirect(nextPage)
            # except:
            messages.success(request, f"You are now logged {user.full_name}.")
            return redirect("home")
    else:
        return render(request, "accounts/login.html")
    return render(request, "accounts/login.html")


def Register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            # Check if the email already exists
            if Account.objects.filter(email=email).exists():
                messages.error(request, "Email address is already registered.")
                return render(request, "accounts/signup.html")
            full_name = form.cleaned_data["full_name"]
            password = form.cleaned_data["password"]
            user = Account.objects.create_user(
                full_name=full_name, email=email, password=password
            )
            user.save()

            profile = UserProfile()
            profile.user = user
            profile.full_name = form.cleaned_data["full_name"]
            profile.email_address = form.cleaned_data["email"]
            profile.profile_photo = "assets/img/profile-img.jpg"
            profile.save()

            # Send activation email
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string(
                "accounts/account_verfication_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = "html"
            send_email.send()
            messages.success(
                request,
                f"Thank you for registering with us. We have sent you a verification email to your email address {email}. Please verify it.",
            )
            return redirect("register")
        else:
            messages.error(request, "Email address is already registered.")

    else:

        pass

    return render(request, "accounts/signup.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated.")
        return redirect("login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


def forget_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = "html"
            send_email.send()

            messages.success(
                request, "Password reset email has been sent to your email address."
            )
            return redirect("login")

        else:
            messages.error(request, "Account does not exist!")
            return redirect("forget_password")
    return render(request, "accounts/forgot-password.html")


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password")
        return redirect("resetPassword")
    else:
        messages.error(request, "This link has been expired!")
        return redirect("login")


def resetPassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("login")
        else:
            messages.error(request, "Password do not match!")
            return redirect("resetPassword")
    else:
        return render(request, "accounts/reset.html")


def update_profile(request):
    if request.method == "GET":
        profile = UserProfile.objects.get(user=request.user)
        print(profile.full_name, "profle")
        context = {"profile": profile}
        return render(request, "others/profile.html", context)

    else:
        profile = get_object_or_404(UserProfile, user=request.user)

        try:

            profile.full_name = request.POST.get("full_name")
            profile.phone_number = request.POST.get("phone_number")
            profile.email_address = request.POST.get("email_address")
            profile.notes = request.POST.get("notes")
            profile.facebook = request.POST.get("facebook")
            profile.twitter = request.POST.get("twitter")
            profile.google_plus = request.POST.get("google_plus")
            profile.instagram = request.POST.get("instagram")
            profile_photo = request.FILES.get("profile_photo")

            if profile_photo:
                profile.profile_photo = profile_photo

            # Save the profile instance
            profile.save()
            messages.success(request, "Profile hass been updated.")

            return redirect("profile")

        except:

            return redirect("profile")


def change_password(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confrim_password"]

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "The current password is incorrect.")
            return redirect("profile")

        if new_password != confirm_password:
            messages.error(
                request, "The new password and confirm password do not match."
            )
            return redirect("profile")

        user.set_password(new_password)
        user.save()

        # Keep the user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Your password has been successfully changed.")
        return redirect("profile")

    else:
        return render(request, "others/profile.html")
