from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "age",
        "can_be_contacted",
        "can_data_be_shared",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields":
                                               ("age",
                                                "can_be_contacted",
                                                "can_data_be_shared",)
                                               }),
                                       )
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields":
                                                       ("age",
                                                        "can_be_contacted",
                                                        "can_data_be_shared",)
                                                       }),
                                               )


admin.site.register(CustomUser, CustomUserAdmin)
