from random import randint
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm, VerifyEmailForm, AddressForm, PasswordResetRequestForm, \
    PasswordVerifyForm, SetNewPasswordForm, EditProfileForm
from .models import User, EmailVerification, PasswordResetCode


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home:home')
        return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    user = request
    logout(user)
    return redirect('home:home')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.is_active = False
                user.set_password(form.cleaned_data.get('password1'))
                user.fullname = form.cleaned_data.get('username')
                user.save()
                code = randint(1000, 9999)
                EmailVerification.objects.create(user=user, code=code)
                send_mail(
                    'تایید ثبت نام',
                    f' کد ثبت نام شما: {code}',
                    'mohammd.ch81m@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return redirect('account:verify-email')

        return render(request, 'account/register.html', {'form': form})


class VerifyEmailView(View):
    def get(self, request):
        form = VerifyEmailForm()
        return render(request, 'account/verify_email.html', {'form': form})

    def post(self, request):
        code = request.POST.get('code')
        form = VerifyEmailForm(data=request.POST)
        if form.is_valid():
            try:
                verification = EmailVerification.objects.get(code=code)
                user = verification.user
                user.is_active = True
                user.save()
                verification.delete()
                login(request, user)
                return redirect('home:home')
            except EmailVerification.DoesNotExist:
                pass

        return render(request, 'account/verify_email.html', {'form': form})


class PasswordResetRequest(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, 'account/password_reset_request.html', {'form': form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            code = randint(1000, 9999)
            PasswordResetCode.objects.create(email=email, code=code)
            request.session['reset_email'] = email
            send_mail(
                'بازیابی رمز عبور',
                f' کد تایید: {code}',
                'mohammd.ch81m@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('account:password-reset-verify')


class PasswordResetVerifyView(View):
    def get(self, request):
        form = PasswordVerifyForm()
        return render(request, 'account/password_verify_code.html', {'form': form})

    def post(self, request):
        form = PasswordVerifyForm(request.POST)
        code = request.POST.get('code')
        if form.is_valid():
            try:
                verify_code = PasswordResetCode.objects.get(code=code)
                verify_code.delete()
                return redirect('account:password-reset-confirm')
            except PasswordResetCode.DoesNotExist:
                form.add_error('code', 'Invalid code')
        return render(request, 'account/password_verify_code.html', {'form': form})


class PasswordConfirmView(View):
    def get(self, request):
        form = SetNewPasswordForm()
        return render(request, 'account/password_reset_confirm.html', {'form': form})

    def post(self, request):
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = request.session.get('reset_email')
            if email:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(cd['new_password'])
                    user.save()
                    return redirect('account:login')
                except User.DoesNotExist:
                    form.add_error(None, 'Invalid email')
        return render(request, 'account/password_reset_confirm.html', {'form': form})


class EditProfileView(View):
    def get(self, request):
        user = request.user
        form = EditProfileForm(instance=user)
        return render(request, 'account/edit_profile.html', {'form': form})

    def post(self, request):
        user = request.user
        form = EditProfileForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:home')

        return render(request, 'account/edit_profile.html', {'form': form})


class AddressView(View):
    def post(self, request):
        form = AddressForm(data=request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('home:home')
        return render(request, 'account/add_address.html', {'form': form})

    def get(self, request):
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form})
