from django.urls import path
from . import views


urlpatterns = [
    path("incomes/", views.IncomesView.as_view(), name="incomes"),
    path("incomes/delete/<int:pk>/", views.IncomesDelete.as_view(), name="delete-incomes"),
    path("incomes/categories/", views.IncomesCategoryView.as_view(), name="incomes-categories"),
    path("incomes/categories/delete/<int:pk>/", views.IncomesCategoryDelete.as_view(), name="delete-incomes-category"),
    
    path("expenses/", views.ExpensesView.as_view(), name="expenses"),
    path("expenses/delete/<int:pk>/", views.ExpensesDelete.as_view(), name="delete-expenses"),
    path("expenses/categories/", views.ExpensesCategoryView.as_view(), name="expenses-categories"),
    path("expenses/categories/delete/<int:pk>/", views.ExpensesCategoryDelete.as_view(), name="delete-expenses-category"),

    path("summary/", views.SummaryView.as_view(), name="summary"),
    path("summary/<int:year>/<int:month>/", views.SummaryView.as_view(), name="summary_by_month"),
    
]