from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal 
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

class MonthlySummaryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user) 
        self.income_category = IncomesCategory.objects.create(user=self.user, category='Salary')
        self.expense_category = ExpensesCategory.objects.create(user=self.user, category='Food')
        self.summary_url = reverse('categories_summary_by_month', args=[2024, 1])

    def test_monthly_summary(self):
        Incomes.objects.create(
            user=self.user,
            category=self.income_category,
            amount=Decimal('1000.00'),
            description='Monthly salary',
            date='2024-01-01'
        )
        Expenses.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('200.00'),
            description='Grocery shopping',
            date='2024-01-02'
        )
        
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('income_by_category', response.data)
        self.assertIn('expense_by_category', response.data)
        self.assertEqual(len(response.data['income_by_category']), 1)
        self.assertEqual(len(response.data['expense_by_category']), 1)
        
    def test_monthly_summary_without_data(self):
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('income_by_category', response.data)
        self.assertIn('expense_by_category', response.data)
        self.assertEqual(len(response.data['income_by_category']), 0)
        self.assertEqual(len(response.data['expense_by_category']), 0)
    def test_monthly_summary_without_authentication(self):
        self.client.logout()
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('income_by_category', response.data)
        self.assertNotIn('expense_by_category', response.data)
    def test_monthly_summary_with_invalid_date(self):
        invalid_summary_url = reverse('categories_summary_by_month', args=[2024, 13])
        response = self.client.get(invalid_summary_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('income_by_category', response.data)
        self.assertNotIn('expense_by_category', response.data)
    def test_monthly_summary_with_no_data(self):
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('income_by_category', response.data)
        self.assertIn('expense_by_category', response.data)
        self.assertEqual(len(response.data['income_by_category']), 0)
        self.assertEqual(len(response.data['expense_by_category']), 0)
    def test_monthly_summary_with_multiple_categories(self):
        income_category2 = IncomesCategory.objects.create(user=self.user, category='Freelance')
        expense_category2 = ExpensesCategory.objects.create(user=self.user, category='Transport')
        
        Incomes.objects.create(
            user=self.user,
            category=self.income_category,
            amount=Decimal('1000.00'),
            description='Monthly salary',
            date='2024-01-01'
        )
        Incomes.objects.create(
            user=self.user,
            category=income_category2,
            amount=Decimal('500.00'),
            description='Freelance project',
            date='2024-01-15'
        )
        Expenses.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('200.00'),
            description='Grocery shopping',
            date='2024-01-02'
        )
        Expenses.objects.create(
            user=self.user,
            category=expense_category2,
            amount=Decimal('100.00'),
            description='Bus ticket',
            date='2024-01-10'
        )
        
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['income_by_category']), 2)
        self.assertEqual(len(response.data['expense_by_category']), 2)
    def test_monthly_summary_with_no_incomes(self):
        Expenses.objects.create(
            user=self.user,
            category=self.expense_category,
            amount=Decimal('200.00'),
            description='Grocery shopping',
            date='2024-01-02'
        )
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('income_by_category', response.data)
        self.assertIn('expense_by_category', response.data)
        self.assertEqual(len(response.data['income_by_category']), 0)
        self.assertEqual(len(response.data['expense_by_category']), 1)

class AdminUserTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.client.force_authenticate(user=self.admin_user) 
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_url = reverse('admin-user-list-create')

    def test_list_users(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], 'admin')
        self.assertEqual(response.data[1]['username'], 'testuser')

    def test_create_user(self):
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'newuser@example.com'}
        response = self.client.post(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username='newuser').username, 'newuser')

    def test_create_user_without_password(self):
        data = {'username': 'newuser', 'email': 'newuser@example.com'}
        response = self.client.post(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
    def test_create_user_without_authentication(self):
        self.client.logout()
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 2)
    def test_create_user_with_existing_username(self):
        data = {'username': 'testuser', 'password': 'newpassword'}
        response = self.client.post(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
    def test_get_user_detail(self):
        user_detail_url = reverse('admin-user-detail', args=[self.user.id])
        response = self.client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    def test_get_non_existent_user_detail(self):
        user_detail_url = reverse('admin-user-detail', args=[999])
        response = self.client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserChangePasswordTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user) 
        self.change_password_url = reverse('change_password')

    def test_change_password(self):
        data = {'new_password': 'newpassword', 'confirm_password': 'newpassword'}
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))

    def test_change_password_with_wrong_old_password(self):
        data = {'old_password': 'wrongpassword', 'new_password': 'newpassword'}
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpassword'))

    def test_change_password_without_authentication(self):
        self.client.logout()
        data = {'old_password': 'testpassword', 'new_password': 'newpassword'}
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password_with_empty_new_password(self):
        data = {'old_password': 'testpassword', 'new_password': ''}
        response = self.client.post(self.change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TokenTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token_url = reverse('get_token')
        self.refresh_url = reverse('refresh')

    def test_obtain_token(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_with_invalid_credentials(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.token_url, data)
        data = {'refresh': response.data['refresh']}
        response = self.client.post(self.refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_token_without_authentication(self):
        self.client.logout()
        data = {'refresh': 'valid_refresh_token'}
        response = self.client.post(self.refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_refresh_token_with_invalid_token(self):
        data = {'refresh': 'invalid_token'}
        response = self.client.post(self.refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.registration_url = reverse('register')

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'last_name': 'User',
            'first_name': 'New'
        }
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')
    def test_user_registration_with_missing_fields(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
    def test_user_registration_with_invalid_email(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'invalid-email',
            'last_name': 'User',
            'first_name': 'New'
        }
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


