from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Expense, Income, Budget


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["amount", "category", "description", "date"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["amount", "source", "description", "date"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category", "amount", "month"]
        widgets = {"month": forms.DateInput(attrs={"type": "date"})}

    category = forms.ChoiceField(choices=Expense.CATEGORY_CHOICES)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
