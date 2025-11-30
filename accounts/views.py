from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import (
    LoginForm,
    UserRegistrationForm,
    UpdateUserForm,
    UpdateProfileForm
)
from .models import Profile


@login_required
def profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass

        if user is None or user.id == request.user.id:
            user_form = UpdateUserForm(
                instance=request.user,
                data=request.POST
            )
            profile_form = UpdateProfileForm(
                instance=request.user.profile,
                data=request.POST
            )

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile was updated successfully')
        else:
            messages.error(request, 'User with given email already exists')

        return redirect('profile')

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(
        request,
        'accounts/profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            cf = user_form.cleaned_data
            email = cf['email']
            password = cf['password']
            password2 = cf['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'User with given email already exists')
                    return render(
                        request,
                        'accounts/register.html',
                        {'user_form': user_form}
                    )

                # Create user
                new_user = User.objects.create_user(
                    first_name=cf['first_name'],
                    last_name=cf['last_name'],
                    username=email,
                    email=email,
                    password=password
                )

                # Create profile
                Profile.objects.create(user=new_user)

                return render(
                    request,
                    'accounts/register_done.html',
                    {'new_user': new_user}
                )

            else:
                messages.error(request, "Passwords don't match")
                return render(
                    request,
                    'accounts/register.html',
                    {'user_form': user_form}
                )

    else:
        user_form = UserRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'user_form': user_form}
    )


# --------------------------------------
# ✅ ADDED USER LOGIN VIEW
# --------------------------------------
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            password = cd['password']

            # Get user by email
            try:
                user_record = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password')
                return render(request, 'accounts/login.html', {'form': form})

            # Authenticate user
            user = authenticate(
                request,
                username=user_record.username,
                password=password
            )

            if user is None:
                messages.error(request, 'Invalid email or password')
                return render(request, 'accounts/login.html', {'form': form})

            # Login user
            login(request, user)
            return redirect('/meals/')   # product → meal

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to get user by email
        try:
            user_record = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(
            request,
            username=user_record.username,
            password=password
        )

        if user is None:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Login user
        login(request, user)

        return Response(
            {
                "detail": "Login successful.",
                "redirect_to": "/meals/"   # product → meal
            },
            status=status.HTTP_200_OK
        )
