from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer, IncomesCategorySerializer, ExpensesCategorySerializer, \
    IncomesSerializer, ExpensesSerializer, SummarySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Incomes, Expenses, IncomesCategory, ExpensesCategory, Summary

# Role info
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
        })
    
# User view
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# przychody kategorie
class IncomesCategoryView(generics.ListCreateAPIView):
    serializer_class = IncomesCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return IncomesCategory.objects.filter(user=user)
    
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
        return ExpensesCategory.objects.filter(user=user)

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

