from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email
         and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=email

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email
         and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="ایمیل",
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    username = models.CharField(max_length=80, default='-', verbose_name='نام کاربری')
    fullname = models.CharField(max_length=50, verbose_name='نام و نام خانوادگی')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر ها'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    code = models.IntegerField(default=0, editable=False, verbose_name='کد')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'تاییدیه ایمیل'
        verbose_name_plural = 'تاییدیه ایمیل ها'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='کاربر')
    full_name = models.CharField(max_length=50, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    phone = models.CharField(max_length=12, verbose_name='شماره تماس')
    address = models.CharField(max_length=300, verbose_name='آدرس')
    postal_code = models.CharField(max_length=15, verbose_name='کد پستی')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'


class PasswordResetCode(models.Model):
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    code = models.IntegerField(default=0, editable=False, verbose_name='کد')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریح ایجاد')

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'بازیابی رمز عبور'
        verbose_name_plural = 'بازیابی رمز های عوبر'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    username = models.CharField(max_length=80, verbose_name='نام کاربری')
    email = models.EmailField(default='-', verbose_name='ایمیل')
    fullname = models.CharField(max_length=80, verbose_name='نام و نام خانوادگی')
    image = models.ImageField(upload_to='img/profiles', blank=True, verbose_name='تصویر')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
