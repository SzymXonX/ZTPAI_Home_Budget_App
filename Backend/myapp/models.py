from django.db import models
from django.contrib.auth.models import User


class IncomesCategory(models.Model):
    """
    **Model reprezentujący kategorię przychodów finansowych.**

    Każda kategoria jest unikalna dla danego użytkownika, co pozwala na personalizację.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Użytkownik, do którego należy ta kategoria przychodów." 
    )
    category = models.CharField(
        max_length=255,
        help_text="Nazwa kategorii przychodu (np. 'Wynagrodzenie', 'Premia')." 
    )

    class Meta:
        verbose_name = "Kategoria Przychodu" 
        verbose_name_plural = "Kategorie Przychodów"
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} - {self.category}"
    
class ExpensesCategory(models.Model):
    """
    **Model reprezentujący kategorię wydatków finansowych.**

    Podobnie jak w przypadku przychodów, każda kategoria jest przypisana do konkretnego użytkownika.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Użytkownik, do którego należy ta kategoria wydatków." 
    )
    category = models.CharField(
        max_length=255,
        help_text="Nazwa kategorii wydatku (np. 'Jedzenie', 'Transport', 'Rozrywka')." 
    )

    class Meta:
        verbose_name = "Kategoria Wydatku"
        verbose_name_plural = "Kategorie Wydatków"

    def __str__(self):
        return f"{self.user.username} - {self.category}"

class Incomes(models.Model):
    """
    **Model reprezentujący pojedynczy wpis przychodu dla użytkownika.**

    Przychód jest powiązany z kategorią i zawiera informacje o kwocie, dacie i opisie.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='incomes',
        help_text="Użytkownik, do którego należy ten przychód."
    )
    category = models.ForeignKey(
        IncomesCategory,
        on_delete=models.CASCADE,
        help_text="Kategoria, do której przypisany jest ten przychód." 
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Kwota przychodu (np. 1500.00)." 
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Opcjonalny, szczegółowy opis przychodu." 
    )
    date = models.DateField(
        help_text="Data uzyskania przychodu (format YYYY-MM-DD)." 
    )

    class Meta:
        verbose_name = "Przychód"
        verbose_name_plural = "Przychody"
        ordering = ['-date'] 

    def __str__(self):
        return f"{self.user.username} - {self.category.category} - {self.amount} - {self.date}"

class Expenses(models.Model):
    """
    **Model reprezentujący pojedynczy wpis wydatku dla użytkownika.**

    Wydatek jest powiązany z kategorią i zawiera informacje o kwocie, dacie i opisie.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses',
        help_text="Użytkownik, do którego należy ten wydatek." 
    )
    category = models.ForeignKey(
        ExpensesCategory,
        on_delete=models.CASCADE,
        help_text="Kategoria, do której przypisany jest ten wydatek."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Kwota wydatku (np. 50.00)." 
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Opcjonalny, szczegółowy opis wydatku."
    )
    date = models.DateField(
        help_text="Data poniesienia wydatku (format YYYY-MM-DD)." 
    )
    
    class Meta:
        verbose_name = "Wydatek"
        verbose_name_plural = "Wydatki"
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.category.category} - {self.amount} - {self.date}"
    