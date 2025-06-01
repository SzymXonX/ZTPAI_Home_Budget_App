from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import Coalesce 
from decimal import Decimal
from .serializers import UserSerializer, IncomesCategorySerializer, ExpensesCategorySerializer, \
    IncomesSerializer, ExpensesSerializer, SummarySerializer, UserProfileSerializer, ChangePasswordSerializer, UserAdminSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Incomes, Expenses, IncomesCategory, ExpensesCategory, Summary


# Role info
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })

    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            return Response(serializer.data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            return Response({"message": "Hasło zostało pomyślnie zmienione."}, status=status.HTTP_200_OK)

# User view
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class AdminUserListView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('username')
    permission_classes = [IsAuthenticated, IsAdminUser] 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSerializer 
        return UserAdminSerializer 

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer 
    permission_classes = [IsAuthenticated, IsAdminUser] 
    lookup_field = 'pk' 

class AdminChangeUserPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        try:
            user_to_change = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Użytkownik nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            return Response({"detail": "Wymagane jest nowe hasło i jego potwierdzenie."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"detail": "Nowe hasła nie są zgodne."}, status=status.HTTP_400_BAD_REQUEST)

        user_to_change.set_password(new_password)
        user_to_change.save()
        return Response({"message": f"Hasło użytkownika '{user_to_change.username}' zostało pomyślnie zmienione."}, status=status.HTTP_200_OK)





# przychody kategorie
class IncomesCategoryView(generics.ListCreateAPIView):
    serializer_class = IncomesCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return IncomesCategory.objects.filter(user=user).order_by('category')
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)
class IncomesCategoryDelete(generics.DestroyAPIView):
    serializer_class = IncomesCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return IncomesCategory.objects.filter(user=user)
    

# wydatki kategorie
class ExpensesCategoryView(generics.ListCreateAPIView):
    serializer_class = ExpensesCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ExpensesCategory.objects.filter(user=user).order_by('category')

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)
class ExpensesCategoryDelete(generics.DestroyAPIView):
    serializer_class = ExpensesCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ExpensesCategory.objects.filter(user=user)


# przychody
class IncomesView(generics.ListCreateAPIView):
    serializer_class = IncomesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Incomes.objects.filter(user=user)

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')

        if year and month:
            queryset = queryset.filter(date__year=year, date__month=month)

        return queryset.order_by('-date')
    
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class IncomesDelete(generics.DestroyAPIView):
    serializer_class = IncomesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Incomes.objects.filter(user=user)


# wydatki
class ExpensesView(generics.ListCreateAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Expenses.objects.filter(user=user)

        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        
        if year and month:
            queryset = queryset.filter(date__year=year, date__month=month)

        return queryset.order_by('-date')
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class ExpensesDelete(generics.DestroyAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expenses.objects.filter(user=user)
    


class MonthlySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        user = request.user

        incomes_summary_raw = Incomes.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        ).values('category__category').annotate(total_amount=Coalesce(Sum('amount'), Decimal('0.00')))

        expenses_summary_raw = Expenses.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        ).values('category__category').annotate(total_amount=Coalesce(Sum('amount'), Decimal('0.00')))

        income_by_category = {item['category__category']: item['total_amount'] for item in incomes_summary_raw}
        expense_by_category = {item['category__category']: item['total_amount'] for item in expenses_summary_raw}

        sorted_income_by_category_list = sorted(
            [(item['category__category'], item['total_amount']) for item in incomes_summary_raw],
            key=lambda x: x[1],
            reverse=True
        )
        income_by_category_ordered = {k: v for k, v in sorted_income_by_category_list}


        sorted_expense_by_category_list = sorted(
            [(item['category__category'], item['total_amount']) for item in expenses_summary_raw],
            key=lambda x: x[1],
            reverse=True
        )
        expense_by_category_ordered = {k: v for k, v in sorted_expense_by_category_list}

        response_data = {
            'year': year,
            'month': month,
            'income_by_category': income_by_category_ordered,
            'expense_by_category': expense_by_category_ordered,
        }

        return Response(response_data, status=status.HTTP_200_OK)

# podsumowanie
class SummaryView(generics.RetrieveAPIView):
    serializer_class = SummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Summary.objects.filter(user=user)

    def get(self, request, year, month, format=None):
        user = request.user
        
        summary = Summary.objects.filter(
            user=user,
            year=year,
            month=month 
        ).first()

        if summary:
            serializer = SummarySerializer(summary)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'No summary found for the given year and month.',
                'year': year,
                'month': month,
                'total_income': '0.00',
                'total_expense': '0.00',
                'balance': '0.00'
            }, status=status.HTTP_404_NOT_FOUND)

