from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from myapp.models import IncomesCategory, ExpensesCategory, Incomes, Expenses

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(IncomesCategory)
admin.site.register(ExpensesCategory)
admin.site.register(Incomes)
admin.site.register(Expenses)
