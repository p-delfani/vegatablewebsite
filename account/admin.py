from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerification, Address, PasswordResetCode, Profile
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("email", "is_admin", 'username')
    list_filter = ("is_admin",)
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("اطلاعات شخصی", {"fields": ["fullname", 'username']}),
        ("دسترسی ها", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", 'username', "fullname", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('email', 'address'[:10])


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(EmailVerification)
admin.site.register(PasswordResetCode)
admin.site.register(Profile)
