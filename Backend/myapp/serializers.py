from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Incomes, Expenses, IncomesCategory, ExpensesCategory

class UserSerializer(serializers.ModelSerializer):
    """
    **Serializator do rejestracji nowego użytkownika.**

    Używany do tworzenia nowego konta użytkownika, wymagając nazwy użytkownika,
    adresu e-mail, hasła, imienia i nazwiska.
    """
    username = serializers.CharField(
        max_length=150,
        help_text="Unikalna nazwa użytkownika (login)."
    )
    email = serializers.EmailField(
        help_text="Adres e-mail użytkownika. Musi być unikalny."
    )
    password = serializers.CharField(
        write_only=True,
        help_text="Hasło użytkownika. Jest wymagane i zapisywane tylko w trybie zapisu (nie jest zwracane)."
    )
    first_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True,
        help_text="Imię użytkownika (opcjonalne)."
    )
    last_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True,
        help_text="Nazwisko użytkownika (opcjonalne)."
    )

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {"password": {"write_only": True}}
        
    def validate_username(self, value):
        if len(value) <= 3:
            raise serializers.ValidationError("Nazwa użytkownika musi mieć więcej niż 3 znaki.")

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Nazwa użytkownika jest już zajęta.")
        
        return value

    def validate(self, data):
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    **Serializator dla profilu użytkownika.**

    Używany do pobierania i aktualizacji podstawowych informacji o zalogowanym użytkowniku.
    Można zaktualizować nazwę użytkownika, imię, nazwisko i adres e-mail.
    """
    username = serializers.CharField(
        max_length=150, required=True,
        help_text="Unikalna nazwa użytkownika (login)."
    )
    first_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True,
        help_text="Imię użytkownika (opcjonalne)."
    )
    last_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True,
        help_text="Nazwisko użytkownika (opcjonalne)."
    )
    email = serializers.EmailField(
        required=True,
        help_text="Adres e-mail użytkownika. Musi być unikalny."
    )

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
    """
    **Serializator do zmiany hasła użytkownika.**

    Wymaga podania nowego hasła i jego potwierdzenia.
    """
    new_password = serializers.CharField(
        required=True, write_only=True,
        help_text="Nowe hasło użytkownika. Musi spełniać wymagania bezpieczeństwa."
    )
    confirm_password = serializers.CharField(
        required=True, write_only=True,
        help_text="Potwierdzenie nowego hasła. Musi być identyczne z 'new_password'."
    )

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
    """
    **Serializator do zarządzania użytkownikami przez administratora.**

    Pozwala administratorom na przeglądanie i aktualizowanie pełnych informacji o użytkownikach,
    w tym ich statusów (`is_staff`, `is_superuser`, `is_active`).
    """
    username = serializers.CharField(
        max_length=150,
        help_text="Unikalna nazwa użytkownika (login)."
    )
    email = serializers.EmailField(
        required=False, allow_blank=True,
        help_text="Adres e-mail użytkownika."
    )
    first_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True,
        help_text="Imię użytkownika."
    )
    last_name = serializers.CharField(
        max_length=150, required=False, allow_blank=True,
        help_text="Nazwisko użytkownika."
    )
    is_staff = serializers.BooleanField(
        help_text="Określa, czy użytkownik ma dostęp do panelu administracyjnego."
    )
    is_superuser = serializers.BooleanField(
        help_text="Określa, czy użytkownik ma wszystkie uprawnienia bez jawnego przypisywania."
    )
    is_active = serializers.BooleanField(
        help_text="Określa, czy konto użytkownika jest aktywne."
    )
    date_joined = serializers.DateTimeField(
        read_only=True,
        help_text="Data i czas rejestracji użytkownika."
    )
    last_login = serializers.DateTimeField(
        read_only=True,
        help_text="Data i czas ostatniego logowania użytkownika."
    )

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
    """
    **Serializator dla kategorii przychodów.**

    Używany do tworzenia, przeglądania i usuwania kategorii,
    do których użytkownik może przypisywać swoje przychody.
    """
    id = serializers.IntegerField(read_only=True, help_text="Unikalny identyfikator kategorii.")
    user = serializers.PrimaryKeyRelatedField(read_only=True, help_text="ID użytkownika, do którego należy kategoria.")
    category = serializers.CharField(
        max_length=255,
        help_text="Nazwa kategorii przychodu (np. 'Wynagrodzenie', 'Premia'). Musi być unikalna dla danego użytkownika."
    )

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
    """
    **Serializator dla kategorii wydatków.**

    Używany do tworzenia, przeglądania i usuwania kategorii,
    do których użytkownik może przypisywać swoje wydatki.
    """
    id = serializers.IntegerField(read_only=True, help_text="Unikalny identyfikator kategorii.")
    user = serializers.PrimaryKeyRelatedField(read_only=True, help_text="ID użytkownika, do którego należy kategoria.")
    category = serializers.CharField(
        max_length=255,
        help_text="Nazwa kategorii wydatku (np. 'Jedzenie', 'Transport'). Musi być unikalna dla danego użytkownika."
    )

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
    """
    **Serializator dla pojedynczego przychodu.**

    Służy do tworzenia, wyświetlania i usuwania danych o przychodach.
    Pole `category` przyjmuje ID kategorii, a `category_name` zwraca jej nazwę.
    """
    id = serializers.IntegerField(read_only=True, help_text="Unikalny identyfikator przychodu.")
    user = serializers.PrimaryKeyRelatedField(read_only=True, help_text="ID użytkownika, do którego należy ten przychód.")
    category_name = serializers.CharField(
        source='category.category', read_only=True,
        help_text="Nazwa kategorii przychodu, do której należy ten przychód (tylko do odczytu)."
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=IncomesCategory.objects.all(),
        help_text="ID kategorii przychodu, do której przypisany jest ten przychód. Wymagane."
    )
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Kwota przychodu. Musi być dodatnia."
    )
    description = serializers.CharField(
        required=False, allow_blank=True,
        help_text="Opcjonalny szczegółowy opis przychodu."
    )
    date = serializers.DateField(
        help_text="Data uzyskania przychodu w formacie YYYY-MM-DD."
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
    """
    **Serializator dla pojedynczego wydatku.**

    Służy do tworzenia, wyświetlania i usuwania danych o wydatkach.
    Pole `category` przyjmuje ID kategorii, a `category_name` zwraca jej nazwę.
    """
    id = serializers.IntegerField(read_only=True, help_text="Unikalny identyfikator wydatku.")
    user = serializers.PrimaryKeyRelatedField(read_only=True, help_text="ID użytkownika, do którego należy ten wydatek.")
    category_name = serializers.CharField(
        source='category.category', read_only=True,
        help_text="Nazwa kategorii wydatku, do której należy ten wydatek (tylko do odczytu)."
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=ExpensesCategory.objects.all(),
        help_text="ID kategorii wydatku, do której przypisany jest ten wydatek. Wymagane."
    )
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Kwota wydatku. Musi być dodatnia."
    )
    description = serializers.CharField(
        required=False, allow_blank=True,
        help_text="Opcjonalny szczegółowy opis wydatku."
    )
    date = serializers.DateField(
        help_text="Data poniesienia wydatku w formacie YYYY-MM-DD."
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

class ErrorSerializer(serializers.Serializer):
    """
    **Serializator dla ogólnych odpowiedzi błędów API.**

    Opisuje strukturę odpowiedzi w przypadku ogólnych błędów serwera (np. 400 Bad Request, 401 Unauthorized).
    """
    detail = serializers.CharField(
        help_text="Szczegółowy komunikat o błędzie (np. 'Nieprawidłowe dane uwierzytelniające')."
    )

class ValidationErrorSerializer(serializers.Serializer):
    """
    **Serializator dla błędów walidacji.**

    Opisuje strukturę odpowiedzi w przypadku błędów walidacji danych (np. wymagane pole puste, nieprawidłowy format).
    Zazwyczaj zwraca słownik, gdzie kluczem jest nazwa pola, a wartością lista błędów.
    """
    field_name = serializers.ListField(
        child= serializers.CharField(),
        help_text="Nazwa pola, które wywołało błąd walidacji, wraz z listą komunikatów błędów dla tego pola. "
                  "Przykład: `{'username': ['To pole jest wymagane.']}`"
    )