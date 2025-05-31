from django.urls import path
from . import views


urlpatterns = [
    path("incomes/", views.IncomesView.as_view(), name="incomes"),
    path("expenses/", views.ExpensesView.as_view(), name="expenses"),

    path("incomes/<int:year>/<int:month>/", views.IncomesView.as_view(), name="incomes-list-by-month"),
    path("expenses/<int:year>/<int:month>/", views.ExpensesView.as_view(), name="expenses-list-by-month"),

    path("incomes/delete/<int:pk>/", views.IncomesDelete.as_view(), name="delete-incomes"),
    path("incomes/categories/delete/<int:pk>/", views.IncomesCategoryDelete.as_view(), name="delete-incomes-category"),
    path("expenses/delete/<int:pk>/", views.ExpensesDelete.as_view(), name="delete-expenses"),
    path("expenses/categories/delete/<int:pk>/", views.ExpensesCategoryDelete.as_view(), name="delete-expenses-category"),
    
    path("incomes/categories/", views.IncomesCategoryView.as_view(), name="incomes-categories"),
    path("expenses/categories/", views.ExpensesCategoryView.as_view(), name="expenses-categories"),

    path("summary/", views.SummaryView.as_view(), name="summary"),
    path("summary/<int:year>/<int:month>/", views.SummaryView.as_view(), name="summary_by_month"),
    
    path("categories/summary/<int:year>/<int:month>/", views.MonthlySummaryView.as_view(), name="categories_summary_by_month"),
]