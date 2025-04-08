from django.urls import path
from . import views




urlpatterns = [
    path("incomesCategory/", views.IncomesCategoryView.as_view(), name="incomes-categories"),
    path("incomesCategory/delete/<int:pk>/", views.IncomesCategoryDelete.as_view(), name="delete-incomes-category"),
]