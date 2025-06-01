from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Incomes, Expenses, IncomesCategory, ExpensesCategory, Summary
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {"password": {"write_only": True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Nazwa użytkownika jest już zajęta.")
        return value

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Nowe hasła nie są zgodne."})
        
        return data

    def save(self):
        user = self.context.get('request').user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'is_staff','is_superuser', 'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def validate_username(self, value):
        if self.instance and User.objects.filter(username=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Nazwa użytkownika jest już zajęta.")
        elif not self.instance and User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Nazwa użytkownika jest już zajęta.")
        return value

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance






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
    category_name = serializers.CharField(source='category.category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=IncomesCategory.objects.all()
    )
    
    class Meta:
        model = Incomes
        fields = ['id', 'user', 'category', 'category_name', 'amount', 'description', 'date']
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
    category_name = serializers.CharField(source='category.category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=ExpensesCategory.objects.all()
    )
    
    class Meta:
        model = Expenses
        fields = ['id', 'user', 'category', 'category_name', 'amount', 'description', 'date']
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
        fields = ['id', 'user', 'total_income', 'total_expense', 'balance', 'year', 'month']
        extra_kwargs = {'user': {'read_only': True}}