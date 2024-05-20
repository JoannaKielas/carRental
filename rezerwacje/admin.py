from django.contrib import admin
from rezerwacje.models import Auto, Rezerwacja, Account
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Auto)
admin.site.register(Rezerwacja)
admin.site.register(Account, AccountAdmin)
# Register your models here.
