from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Incomes, Expenses, IncomesCategory, ExpensesCategory, Summary

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {"password": {"write_only": True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class IncomesCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomesCategory
        fields = ['id', 'user', 'category']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = validated_data['user']
        category = validated_data['category']
        
        if IncomesCategory.objects.filter(user=user, category=category).exists():
            raise serializers.ValidationError("Category already exists for this user.")
        
        instance = IncomesCategory.objects.create(user=user, category=category)
        return instance

class ExpensesCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpensesCategory
        fields = ['id', 'user', 'category']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = validated_data['user']
        category = validated_data['category']

        if ExpensesCategory.objects.filter(user=user, category=category).exists():
            raise serializers.ValidationError("Category already exists for this user.")
        
        instance = ExpensesCategory.objects.create(user=user, category=category)
        return instance
    

    
class IncomesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incomes
        fields = ['id', 'user', 'category', 'amount', 'description', 'date']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = validated_data['user']
        category = validated_data['category']
        amount = validated_data['amount']
        description = validated_data['description']
        date = validated_data['date']

        if amount < 0:
            raise serializers.ValidationError("Amount cannot be negative.")

        instance = Incomes.objects.create(user=user, category=category, amount=amount, description=description, date=date)
        return instance
    
class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ['id', 'user', 'category', 'amount', 'description', 'date']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = validated_data['user']
        category = validated_data['category']
        amount = validated_data['amount']
        description = validated_data['description']
        date = validated_data['date']

        if amount < 0:
            raise serializers.ValidationError("Amount cannot be negative.")

        instance = Expenses.objects.create(user=user, category=category, amount=amount, description=description, date=date)
        return instance
    


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['id', 'user', 'total_income', 'total_expense', 'balance']
        extra_kwargs = {'user': {'read_only': True}}