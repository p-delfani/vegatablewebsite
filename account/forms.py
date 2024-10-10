from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, EmailVerification, Address, PasswordResetCode, Profile


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تایید رمز عبور", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("رمز عبور اشتباه است")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", 'username', "password", "is_active"]


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}), )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}))

    def clean(self):
        self.cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise ValidationError("رمز عبور یا ایمیل اشتباه است")
        return self.cleaned_data


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}), )
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
    fullname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'تایید رمز عبور'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("این نام کاربری وجود دارد")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل وجود دارد")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)

        if len(password1) < 8:
            raise ValidationError('رمز عبور حداقل باید 8 کاراکتر باشد')

        return password1

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if password2 is None:
            raise ValidationError('این فیلد الزامی است')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("رمز عبور اشتباه است")

        return cleaned_data


class VerifyEmailForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'کد تایید'}))

    def clean_code(self):
        code = self.cleaned_data['code']
        if EmailVerification.objects.filter(code=code) is None:
            raise ValidationError('کد تایید اشتباه است')


class AddressForm(forms.ModelForm):
    user = forms.IntegerField(required=False)

    class Meta:
        model = Address
        fields = ('full_name', 'email', 'phone', 'address', 'postal_code')

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شمار تماس'
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'آدرس'
            }),

            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کد پستی'
            })
        }


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}), )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("ایمیل نامعتبر است.")
        return email


class PasswordVerifyForm(forms.Form):
    code = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'کد تایید را وارد کنید'}))

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            if not PasswordResetCode.objects.filter(code=code).exists():
                raise forms.ValidationError("کد نامعتبر است")
        except PasswordResetCode.DoesNotExist:
            raise forms.ValidationError("کد نامعتبر است")

        return code


class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("پسورد اشتباه است.")
        return cleaned_data

    def clean_password1(self):
        new_password = self.cleaned_data.get('new_password')
        validate_password(new_password)

        if len(new_password) < 8:
            raise ValidationError('رمز عبور باید حداقل 8 کاراکتر داشته باشد')

        return new_password


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('email', 'username', 'fullname', 'image')
        error_messages = {
            'email': {
                'unique': "ایمیل وارد شده قبلا ثبت شده است.",
            },
        }
        widgets = {

            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),

            'fullname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'تصویر پروفایل'
            }),

        }
