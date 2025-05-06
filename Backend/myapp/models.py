from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class IncomesCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.category}"
    
class ExpensesCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.category}"

class Incomes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    category = models.ForeignKey(IncomesCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.category.category} - {self.amount} - {self.date}"

class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(ExpensesCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.category.category} - {self.amount} - {self.date}"
    
class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summary', unique=True)
    total_income = models.DecimalField(max_digits=10, decimal_places=2)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.total_income} - {self.total_expense} - {self.balance}"


