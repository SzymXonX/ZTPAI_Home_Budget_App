from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import Coalesce 
from decimal import Decimal
import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .serializers import UserSerializer, IncomesCategorySerializer, ExpensesCategorySerializer, \
    IncomesSerializer, ExpensesSerializer, UserProfileSerializer, ChangePasswordSerializer, UserAdminSerializer, ValidationErrorSerializer, ErrorSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Incomes, Expenses, IncomesCategory, ExpensesCategory

class UserInfoView(APIView):
    """
    **Informacje o profilu użytkownika.**

    Ten endpoint pozwala zalogowanemu użytkownikowi na pobranie swoich podstawowych informacji profilowych
    (`GET`) oraz na aktualizację wybranych danych (`PATCH`).
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Pobierz informacje o profilu zalogowanego użytkownika",
        description="Zwraca szczegółowe dane profilowe aktualnie zalogowanego użytkownika.",
        responses={
            200: UserProfileSerializer,
            401: {'description': 'Brak autoryzacji: użytkownik nie jest zalogowany.'},
        }
    )
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

    @extend_schema(
        summary="Zaktualizuj informacje o profilu zalogowanego użytkownika",
        description="Pozwala na częściową aktualizację danych profilowych zalogowanego użytkownika. "
                    "Możesz zaktualizować takie pola jak 'email', 'first_name', 'last_name'.",
        request=UserProfileSerializer(partial=True),
        responses={
            200: UserProfileSerializer,
            400: ValidationErrorSerializer,
            401: {'description': 'Brak autoryzacji: użytkownik nie jest zalogowany.'},
        }
    )
    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            return Response(serializer.data)

class ChangePasswordView(APIView):
    """
    **Zmiana hasła użytkownika.**

    Endpoint umożliwiający zalogowanemu użytkownikowi zmianę własnego hasła.
    Wymaga podania nowego hasła i jego potwierdzenia.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Zmień hasło zalogowanego użytkownika",
        request=ChangePasswordSerializer,
        responses={
            200: {'description': 'Hasło zostało pomyślnie zmienione.'},
            400: ErrorSerializer,
            401: {'description': 'Brak autoryzacji: użytkownik nie jest zalogowany.'},
        }
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            return Response({"message": "Hasło zostało pomyślnie zmienione."}, status=status.HTTP_200_OK)

class CreateUserView(generics.CreateAPIView):
    """
    **Rejestracja nowego użytkownika.**

    Ten endpoint pozwala na stworzenie nowego konta użytkownika w systemie.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Zarejestruj nowego użytkownika",
        description="Utwórz nowe konto użytkownika. Hasło zostanie zaszyfrowane automatycznie.",
        responses={
            201: UserSerializer,
            400: ValidationErrorSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AdminUserListView(generics.ListCreateAPIView):
    """
    **Zarządzanie użytkownikami (tylko dla administratorów).**

    Ten endpoint pozwala administratorom na pobranie listy wszystkich użytkowników
    w systemie oraz na tworzenie nowych kont użytkowników.
    """
    queryset = User.objects.all().order_by('username')
    permission_classes = [IsAuthenticated, IsAdminUser] 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSerializer 
        return UserAdminSerializer 

    @extend_schema(
        summary="Pobierz listę wszystkich użytkowników (admin)",
        description="Zwraca listę wszystkich użytkowników w systemie, dostępną tylko dla administratorów.",
        responses={
            200: UserAdminSerializer(many=True),
            401: {'description': 'Brak autoryzacji.'},
            403: {'description': 'Brak uprawnień administratora.'},
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Utwórz nowego użytkownika (admin)",
        description="Tworzy nowe konto użytkownika. Dostępne tylko dla administratorów.",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: ValidationErrorSerializer,
            401: {'description': 'Brak autoryzacji.'},
            403: {'description': 'Brak uprawnień administratora.'},
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    **Szczegóły użytkownika (tylko dla administratorów).**

    Ten endpoint pozwala administratorom na pobranie, aktualizację lub usunięcie
    konkretnego użytkownika po jego ID.
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer 
    permission_classes = [IsAuthenticated, IsAdminUser] 
    lookup_field = 'pk' 

    @extend_schema(
        summary="Pobierz szczegóły użytkownika po ID (admin)",
        description="Zwraca szczegółowe dane konkretnego użytkownika. Dostępne tylko dla administratorów.",
        responses={
            200: UserAdminSerializer,
            401: {'description': 'Brak autoryzacji.'},
            403: {'description': 'Brak uprawnień administratora.'},
            404: {'description': 'Użytkownik o podanym ID nie znaleziony.'},
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Zaktualizuj użytkownika po ID (admin)",
        description="Pełna aktualizacja danych użytkownika. Dostępne tylko dla administratorów.",
        request=UserAdminSerializer,
        responses={
            200: UserAdminSerializer,
            400: ValidationErrorSerializer,
            401: {'description': 'Brak autoryzacji.'},
            403: {'description': 'Brak uprawnień administratora.'},
            404: {'description': 'Użytkownik o podanym ID nie znaleziony.'},
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Częściowo zaktualizuj użytkownika po ID (admin)",
        description="Częściowa aktualizacja danych użytkownika. Dostępne tylko dla administratorów.",
        request=UserAdminSerializer(partial=True),
        responses={
            200: UserAdminSerializer,
            400: ValidationErrorSerializer,
            401: {'description': 'Brak autoryzacji.'},
            403: {'description': 'Brak uprawnień administratora.'},
            404: {'description': 'Użytkownik o podanym ID nie znaleziony.'},
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Usuń użytkownika po ID (admin)",
        description="Usuwa konto użytkownika. Dostępne tylko dla administratorów.",
        responses={
            204: {'description': 'Użytkownik został pomyślnie usunięty.'},
            401: {'description': 'Brak autoryzacji.'},
            403: {'description': 'Brak uprawnień administratora.'},
            404: {'description': 'Użytkownik o podanym ID nie znaleziony.'},
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class IncomesCategoryView(generics.ListCreateAPIView):
    """
    **Zarządzanie kategoriami przychodów.**

    Ten endpoint pozwala na pobranie listy wszystkich kategorii przychodów należących
    do zalogowanego użytkownika oraz na tworzenie nowych kategorii.
    """
    serializer_class = IncomesCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return IncomesCategory.objects.filter(user=user).order_by('category')
    
    @extend_schema(
        summary="Pobierz listę kategorii przychodów użytkownika",
        description="Zwraca listę wszystkich zdefiniowanych kategorii przychodów dla zalogowanego użytkownika.",
        responses={
            200: IncomesCategorySerializer(many=True),
            401: {'description': 'Brak autoryzacji.'},
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Utwórz nową kategorię przychodów",
        description="Dodaje nową kategorię przychodów dla zalogowanego użytkownika.",
        request=IncomesCategorySerializer,
        responses={
            201: IncomesCategorySerializer,
            400: ValidationErrorSerializer,
            401: {'description': 'Brak autoryzacji.'},
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)
class IncomesCategoryDelete(generics.DestroyAPIView):
    """
    **Usuwanie kategorii przychodów.**

    Ten endpoint pozwala na usunięcie konkretnej kategorii przychodów
    należącej do zalogowanego użytkownika po jej ID.
    """
    serializer_class = IncomesCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return IncomesCategory.objects.filter(user=user)
    
    @extend_schema(
        summary="Usuń kategorię przychodów",
        description="Usuwa kategorię przychodów. Kategoria musi należeć do zalogowanego użytkownika.",
        parameters=[
            OpenApiParameter(name='pk', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='**ID kategorii** przychodów do usunięcia.', required=True),
        ],
        responses={
            204: {'description': 'Kategoria została pomyślnie usunięta.'},
            401: {'description': 'Brak autoryzacji.'},
            404: {'description': 'Kategoria nie znaleziona lub nie należy do użytkownika.'},
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ExpensesCategoryView(generics.ListCreateAPIView):
    """
    **Zarządzanie kategoriami wydatków.**

    Ten endpoint pozwala na pobranie listy wszystkich kategorii wydatków
    należących do zalogowanego użytkownika oraz na tworzenie nowych kategorii.
    """
    serializer_class = ExpensesCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ExpensesCategory.objects.filter(user=user).order_by('category')

    @extend_schema(
        summary="Pobierz listę kategorii wydatków użytkownika",
        description="Zwraca listę wszystkich zdefiniowanych kategorii wydatków dla zalogowanego użytkownika.",
        responses={
            200: ExpensesCategorySerializer(many=True),
            401: {'description': 'Brak autoryzacji.'},
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Utwórz nową kategorię wydatków",
        description="Dodaje nową kategorię wydatków dla zalogowanego użytkownika.",
        request=ExpensesCategorySerializer,
        responses={
            201: ExpensesCategorySerializer,
            400: ValidationErrorSerializer,
            401: {'description': 'Brak autoryzacji.'},
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)
class ExpensesCategoryDelete(generics.DestroyAPIView):
    """
    **Usuwanie kategorii wydatków.**

    Ten endpoint pozwala na usunięcie konkretnej kategorii wydatków
    należącej do zalogowanego użytkownika po jej ID.
    """
    serializer_class = ExpensesCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ExpensesCategory.objects.filter(user=user)

    @extend_schema(
        summary="Usuń kategorię wydatków",
        description="Usuwa kategorię wydatków. Kategoria musi należeć do zalogowanego użytkownika.",
        parameters=[
            OpenApiParameter(name='pk', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='**ID kategorii** wydatków do usunięcia.', required=True),
        ],
        responses={
            204: {'description': 'Kategoria została pomyślnie usunięta.'},
            401: {'description': 'Brak autoryzacji.'},
            404: {'description': 'Kategoria nie znaleziona lub nie należy do użytkownika.'},
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class IncomesView(generics.ListCreateAPIView):
    """
    **Zarządzanie przychodami.**

    Ten endpoint pozwala na pobranie listy wszystkich przychodów użytkownika
    oraz na dodawanie nowych przychodów.
    Możliwe jest filtrowanie po roku i miesiącu w URL-u.
    """
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
    
    @extend_schema(
        summary="Pobierz listę przychodów użytkownika",
        description="Zwraca listę wszystkich przychodów zalogowanego użytkownika. "
                    "Można filtrować wyniki, podając rok i miesiąc w ścieżce URL.",
        parameters=[
            OpenApiParameter(name='year', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='Rok (np. `2024`) do filtrowania przychodów.', required=False,
                             examples=[OpenApiExample('Bieżący rok', value=2024)]),
            OpenApiParameter(name='month', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='Miesiąc (np. `6` dla czerwca) do filtrowania przychodów.', required=False,
                             examples=[OpenApiExample('Bieżący miesiąc', value=6)]),
        ],
        responses={
            200: IncomesSerializer(many=True),
            401: {'description': 'Brak autoryzacji.'},
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Dodaj nowy przychód",
        description="Dodaje nowy przychód dla zalogowanego użytkownika.",
        request=IncomesSerializer,
        responses={
            201: IncomesSerializer,
            400: ValidationErrorSerializer,
            401: {'description': 'Brak autoryzacji.'},
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class IncomesDelete(generics.DestroyAPIView):
    """
    **Usuwanie przychodu.**

    Ten endpoint pozwala na usunięcie konkretnego przychodu
    należącego do zalogowanego użytkownika po jego ID.
    """
    serializer_class = IncomesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Incomes.objects.filter(user=user)

    @extend_schema(
        summary="Usuń przychód",
        description="Usuwa przychód. Przychód musi należeć do zalogowanego użytkownika.",
        parameters=[
            OpenApiParameter(name='pk', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='**ID przychodu** do usunięcia.', required=True),
        ],
        responses={
            204: {'description': 'Przychód został pomyślnie usunięty.'},
            401: {'description': 'Brak autoryzacji.'},
            404: {'description': 'Przychód nie znaleziony lub nie należy do użytkownika.'},
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ExpensesView(generics.ListCreateAPIView):
    """
    **Zarządzanie wydatkami.**

    Ten endpoint pozwala na pobranie listy wszystkich wydatków użytkownika
    oraz na dodawanie nowych wydatków.
    Możliwe jest filtrowanie po roku i miesiącu w URL-u.
    """
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
    
    @extend_schema(
        summary="Pobierz listę wydatków użytkownika",
        description="Zwraca listę wszystkich wydatków zalogowanego użytkownika. "
                    "Można filtrować wyniki, podając rok i miesiąc w ścieżce URL.",
        parameters=[
            OpenApiParameter(name='year', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='Rok (np. `2024`) do filtrowania wydatków.', required=False,
                             examples=[OpenApiExample('Bieżący rok', value=2024)]),
            OpenApiParameter(name='month', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='Miesiąc (np. `6` dla czerwca) do filtrowania wydatków.', required=False,
                             examples=[OpenApiExample('Bieżący miesiąc', value=6)]),
        ],
        responses={
            200: ExpensesSerializer(many=True),
            401: {'description': 'Brak autoryzacji.'},
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary="Dodaj nowy wydatek",
        description="Dodaje nowy wydatek dla zalogowanego użytkownika.",
        request=ExpensesSerializer,
        responses={
            201: ExpensesSerializer,
            400: ValidationErrorSerializer,
            401: {'description': 'Brak autoryzacji.'},
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class ExpensesDelete(generics.DestroyAPIView):
    """
    **Usuwanie wydatku.**

    Ten endpoint pozwala na usunięcie konkretnego wydatku
    należącego do zalogowanego użytkownika po jego ID.
    """
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expenses.objects.filter(user=user)
    
    @extend_schema(
        summary="Usuń wydatek",
        description="Usuwa wydatek. Wydatek musi należeć do zalogowanego użytkownika.",
        parameters=[
            OpenApiParameter(name='pk', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='**ID wydatku** do usunięcia.', required=True),
        ],
        responses={
            204: {'description': 'Wydatek został pomyślnie usunięty.'},
            401: {'description': 'Brak autoryzacji.'},
            404: {'description': 'Wydatek nie znaleziony lub nie należy do użytkownika.'},
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

class MonthlySummaryView(APIView):
    """
    **Miesięczne podsumowanie przychodów i wydatków.**

    Ten endpoint zwraca zagregowane dane o przychodach i wydatkach dla danego
    roku i miesiąca, pogrupowane według kategorii.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Pobierz miesięczne podsumowanie finansowe (kategorie)",
        description="Oblicza i zwraca sumy przychodów i wydatków, pogrupowane według kategorii, dla określonego miesiąca i roku.",
        parameters=[
            OpenApiParameter(name='year', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='**Rok** (np. `2024`) dla podsumowania.', required=True,
                             examples=[OpenApiExample('Rok 2024', value=2024)]),
            OpenApiParameter(name='month', type=OpenApiTypes.INT, location=OpenApiParameter.PATH,
                             description='**Miesiąc** (np. `6` dla czerwca) dla podsumowania.', required=True,
                             examples=[OpenApiExample('Czerwiec', value=6)]),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'year': {'type': 'integer', 'description': 'Rok podsumowania.'},
                    'month': {'type': 'integer', 'description': 'Miesiąc podsumowania.'},
                    'income_by_category': {
                        'type': 'object',
                        'additionalProperties': {'type': 'string', 'format': 'decimal'},
                        'description': 'Suma przychodów pogrupowana według kategorii (nazwa kategorii: suma kwot).'
                    },
                    'expense_by_category': {
                        'type': 'object',
                        'additionalProperties': {'type': 'string', 'format': 'decimal'},
                        'description': 'Suma wydatków pogrupowana według kategorii (nazwa kategorii: suma kwot).'
                    },
                },
                'example': { 
                    'year': 2024,
                    'month': 6,
                    'income_by_category': {
                        'Wynagrodzenie': '3000.00',
                        'Dodatkowa Praca': '750.00'
                    },
                    'expense_by_category': {
                        'Jedzenie': '800.50',
                        'Transport': '200.00',
                        'Rozrywka': '150.00'
                    }
                }
            },
            401: {'description': 'Brak autoryzacji.'},
        }
    )
    def get(self, request, year, month):
        user = request.user
        try:
            current_year = datetime.datetime.now().year
            if not (1900 <= year <= current_year + 1):
                return Response(
                    {"error": "Invalid year. Year must be between 1900 and the current year + 1."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not (1 <= month <= 12):
                return Response(
                    {"error": "Invalid month. Month must be between 1 and 12."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            datetime.date(year, month, 1)
        except ValueError:
            return Response(
                {"error": "Invalid year or month combination."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
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

        total_income = sum(item['total_amount'] for item in incomes_summary_raw)
        total_expense = sum(item['total_amount'] for item in expenses_summary_raw)

        balance = total_income - total_expense

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
            'total_income': f"{total_income:.2f}",
            'total_expense': f"{total_expense:.2f}",
            'balance': f"{balance:.2f}",
            'income_by_category': income_by_category_ordered,
            'expense_by_category': expense_by_category_ordered,
        }

        return Response(response_data, status=status.HTTP_200_OK)
