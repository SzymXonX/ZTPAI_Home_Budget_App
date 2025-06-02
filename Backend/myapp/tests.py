from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import IncomesCategory, Incomes 
from decimal import Decimal 


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import *

class IncomesCategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user) 
        self.category_url = reverse('incomes-categories')

    def test_create_category(self):
        data = {'category': 'Freelance'}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IncomesCategory.objects.count(), 1)
        self.assertEqual(IncomesCategory.objects.get().category, 'Freelance')

    def test_create_duplicate_category(self):
        IncomesCategory.objects.create(user=self.user, category='Freelance')
        data = {'category': 'Freelance'}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(IncomesCategory.objects.count(), 1)

    def test_create_category_without_authentication(self):
        self.client.logout()
        data = {'category': 'Freelance'}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(IncomesCategory.objects.count(), 0)

    def test_list_categories(self):
        IncomesCategory.objects.create(user=self.user, category='Freelance')
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['category'], 'Freelance')

    def test_delete_category(self):
        category = IncomesCategory.objects.create(user=self.user, category='Freelance')
        delete_url = reverse('delete-incomes-category', args=[category.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(IncomesCategory.objects.count(), 0)

    def test_delete_non_existent_category(self):
        delete_url = reverse('delete-incomes-category', args=[999])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(IncomesCategory.objects.count(), 0)

    def test_delete_category_without_authentication(self):
        category = IncomesCategory.objects.create(user=self.user, category='Freelance')
        self.client.logout()
        delete_url = reverse('delete-incomes-category', args=[category.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(IncomesCategory.objects.count(), 1)

    def test_create_category_with_invalid_data(self):
        data = {'category': ''}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(IncomesCategory.objects.count(), 0)

    def test_create_category_with_long_name(self):
        data = {'category': 'a' * 256}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(IncomesCategory.objects.count(), 0)

    def test_create_category_with_special_characters(self):
        data = {'category': '@Freelance!'}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IncomesCategory.objects.count(), 1)

class ExpensesCategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user) 
        self.category_url = reverse('expenses-categories')

    def test_create_category(self):
        data = {'category': 'Food'}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExpensesCategory.objects.count(), 1)
        self.assertEqual(ExpensesCategory.objects.get().category, 'Food')

    def test_create_duplicate_category(self):
        ExpensesCategory.objects.create(user=self.user, category='Food')
        data = {'category': 'Food'}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ExpensesCategory.objects.count(), 1)

    def test_create_category_without_authentication(self):
        self.client.logout()
        data = {'category': 'Food'}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ExpensesCategory.objects.count(), 0)

    def test_list_categories(self):
        ExpensesCategory.objects.create(user=self.user, category='Food')
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['category'], 'Food')

    def test_delete_category(self):
        category = ExpensesCategory.objects.create(user=self.user, category='Food')
        delete_url = reverse('delete-expenses-category', args=[category.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExpensesCategory.objects.count(), 0)

    def test_delete_non_existent_category(self):
        delete_url = reverse('delete-expenses-category', args=[999])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ExpensesCategory.objects.count(), 0)
        
    def test_delete_category_without_authentication(self):
        category = ExpensesCategory.objects.create(user=self.user, category='Food')
        self.client.logout()
        delete_url = reverse('delete-expenses-category', args=[category.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ExpensesCategory.objects.count(), 1)
    def test_create_category_with_invalid_data(self):
        data = {'category': ''}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ExpensesCategory.objects.count(), 0)

    def test_create_category_with_long_name(self):
        data = {'category': 'a' * 256}
        response = self.client.post(self.category_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ExpensesCategory.objects.count(), 0)

class ExpensesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user) 
        self.category = ExpensesCategory.objects.create(user=self.user, category='Food')
        self.expense_url = reverse('expenses')

    def test_create_expense(self):
        data = {
            'category': self.category.id,
            'amount': Decimal('50.00'),
            'description': 'Grocery shopping',
            'date': '2024-01-01'
        }
        response = self.client.post(self.expense_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expenses.objects.count(), 1)
        expense = Expenses.objects.get()
        self.assertEqual(expense.category, self.category)
        self.assertEqual(expense.amount, Decimal('50.00'))
        self.assertEqual(expense.description, 'Grocery shopping')
        self.assertEqual(str(expense.date), '2024-01-01')

    def test_create_expense_without_authentication(self):
        self.client.logout()
        data = {
            'category': self.category.id,
            'amount': Decimal('50.00'),
            'description': 'Grocery shopping',
            'date': '2024-01-01'
        }
        response = self.client.post(self.expense_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Expenses.objects.count(), 0)

    def test_create_expense_with_invalid_data(self):
        data = {
            'category': self.category.id,
            'amount': Decimal('50.00'),
            'description': '',
            'date': ''
        }
        response = self.client.post(self.expense_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Expenses.objects.count(), 0)

    def test_list_expenses(self):
        Expenses.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('50.00'),
            description='Grocery shopping',
            date='2024-01-01'
        )
        response = self.client.get(self.expense_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_delete_expense(self):
        expense = Expenses.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('50.00'),
            description='Grocery shopping',
            date='2024-01-01'
        )
        delete_url = reverse('delete-expenses', args=[expense.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expenses.objects.count(), 0)
    def test_delete_non_existent_expense(self): 
        delete_url = reverse('delete-expenses', args=[999])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Expenses.objects.count(), 0)
    def test_delete_expense_without_authentication(self):   
        expense = Expenses.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('50.00'),
            description='Grocery shopping',
            date='2024-01-01'
        )
        self.client.logout()
        delete_url = reverse('delete-expenses', args=[expense.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Expenses.objects.count(), 1)

class IncomesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user) 
        self.category = IncomesCategory.objects.create(user=self.user, category='Salary')
        self.income_url = reverse('incomes')

    def test_create_income(self):
        data = {
            'category': self.category.id,
            'amount': Decimal('1000.00'),
            'description': 'Monthly salary',
            'date': '2024-01-01'
        }
        response = self.client.post(self.income_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Incomes.objects.count(), 1)
        income = Incomes.objects.get()
        self.assertEqual(income.category, self.category)
        self.assertEqual(income.amount, Decimal('1000.00'))
        self.assertEqual(income.description, 'Monthly salary')
        self.assertEqual(str(income.date), '2024-01-01')

    def test_create_income_without_authentication(self):
        self.client.logout()
        data = {
            'category': self.category.id,
            'amount': Decimal('1000.00'),
            'description': 'Monthly salary',
            'date': '2024-01-01'
        }
        response = self.client.post(self.income_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Incomes.objects.count(), 0)

    def test_create_income_with_invalid_data(self):
        data = {
            'category': self.category.id,
            'amount': Decimal('1000.00'),
            'description': '',
            'date': ''
        }
        response = self.client.post(self.income_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Incomes.objects.count(), 0)

    def test_list_incomes(self):
        Incomes.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('1000.00'),
            description='Monthly salary',
            date='2024-01-01'
        )
        response = self.client.get(self.income_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_delete_income(self):
        income = Incomes.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('1000.00'),
            description='Monthly salary',
            date='2024-01-01'
        )
        delete_url = reverse('delete-incomes', args=[income.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Incomes.objects.count(), 0)
    def test_delete_non_existent_income(self):
        delete_url = reverse('delete-incomes', args=[999])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Incomes.objects.count(), 0)
    def test_delete_income_without_authentication(self):
        income = Incomes.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('1000.00'),
            description='Monthly salary',
            date='2024-01-01'
        )
        self.client.logout()
        delete_url = reverse('delete-incomes', args=[income.id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Incomes.objects.count(), 1)

class SummaryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.income_category = IncomesCategory.objects.create(user=self.user, category='Salary')
        self.expense_category = ExpensesCategory.objects.create(user=self.user, category='Food')
        self.income = Incomes.objects.create(
            user=self.user,
            category=self.income_category,
            amount=Decimal('1000.00'),
            description='Monthly salary',
            date='2024-01-01'
        )
        self.expense = Expenses.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('200.00'),
            description='Grocery shopping',
            date='2024-01-02'
        )

    def test_get_summary(self):
        url = reverse('summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expenses', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '1000.00')
        self.assertEqual(response.data['total_expenses'], '200.00')
        self.assertEqual(response.data['balance'], '800.00')

    def test_get_summary_by_month(self):
        url = reverse('summary_by_month', args=[2024, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expenses', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '1000.00')
        self.assertEqual(response.data['total_expenses'], '200.00')
        self.assertEqual(response.data['balance'], '800.00')
        
    def test_get_summary_no_data(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.client.force_authenticate(user=new_user)
        url = reverse('summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expenses', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '0.00')
        self.assertEqual(response.data['total_expenses'], '0.00')
        self.assertEqual(response.data['balance'], '0.00')
    def test_get_summary_without_authentication(self):
        self.client.logout()
        url = reverse('summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_get_summary_by_month_without_authentication(self):
        self.client.logout()
        url = reverse('summary_by_month', args=[2024, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_get_summary_by_month_no_data(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.client.force_authenticate(user=new_user)
        url = reverse('summary_by_month', args=[2024, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expenses', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '0.00')
        self.assertEqual(response.data['total_expenses'], '0.00')
        self.assertEqual(response.data['balance'], '0.00')
    def test_get_summary_by_month_invalid_date(self):
        url = reverse('summary_by_month', args=[2024, 13])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_get_summary_by_month_invalid_year(self):
        url = reverse('summary_by_month', args=[2023, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_get_summary_by_month_invalid_month(self):
        url = reverse('summary_by_month', args=[2024, 0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_get_summary_by_month_future_date(self):
        url = reverse('summary_by_month', args=[2025, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_get_summary_by_month_past_date(self):
        url = reverse('summary_by_month', args=[2020, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_get_summary_by_month_no_expenses(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.client.force_authenticate(user=new_user)
        url = reverse('summary_by_month', args=[2024, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expenses', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '0.00')
        self.assertEqual(response.data['total_expenses'], '0.00')
        self.assertEqual(response.data['balance'], '0.00')
    def test_get_summary_by_month_no_incomes(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.client.force_authenticate(user=new_user)
        url = reverse('summary_by_month', args=[2024, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expenses', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '0.00')
        self.assertEqual(response.data['total_expenses'], '0.00')
        self.assertEqual(response.data['balance'], '0.00')
    def test_get_summary_by_month_no_data_for_user(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.client.force_authenticate(user=new_user)
        url = reverse('summary_by_month', args=[2024, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expenses', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '0.00')
        self.assertEqual(response.data['total_expenses'], '0.00')
        self.assertEqual(response.data['balance'], '0.00')
    def test_get_summary_by_month_no_data_for_month(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.client.force_authenticate(user=new_user)
        url = reverse('summary_by_month', args=[2024, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expenses', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '0.00')
        self.assertEqual(response.data['total_expenses'], '0.00')
        self.assertEqual(response.data['balance'], '0.00')
    def test_get_summary_by_month_no_data_for_year(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.client.force_authenticate(user=new_user)
        url = reverse('summary_by_month', args=[2024, 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('total_expenses', response.data)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['total_income'], '0.00')
        self.assertEqual(response.data['total_expenses'], '0.00')
        self.assertEqual(response.data['balance'], '0.00')