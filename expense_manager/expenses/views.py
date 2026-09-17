from decimal import Decimal
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BudgetForm, ExpenseForm, IncomeForm, RegisterForm
from .models import Budget, Expense, Income


def user_expense(request, **kwargs):
    return get_object_or_404(Expense, user=request.user, **kwargs)


def user_income(request, **kwargs):
    return get_object_or_404(Income, user=request.user, **kwargs)


def user_budget(request, **kwargs):
    return get_object_or_404(Budget, user=request.user, **kwargs)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Username or password is incorrect.")

    return render(request, "expenses/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "expenses/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    selected_month = request.GET.get("month")

    if selected_month:
        try:
            year, month = selected_month.split("-")
            year, month = int(year), int(month)
        except (ValueError, AttributeError):
            today = date.today()
            year, month = today.year, today.month
    else:
        today = date.today()
        year, month = today.year, today.month

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "expense":
            form = ExpenseForm(request.POST)
            if form.is_valid():
                expense = form.save(commit=False)
                expense.user = request.user
                expense.save()
                return redirect("home")

        elif form_type == "income":
            form = IncomeForm(request.POST)
            if form.is_valid():
                income = form.save(commit=False)
                income.user = request.user
                income.save()
                return redirect("home")

        elif form_type == "budget":
            form = BudgetForm(request.POST)
            if form.is_valid():
                budget = form.save(commit=False)
                budget.user = request.user
                budget.save()
                return redirect("home")

    expense_form = ExpenseForm()
    income_form = IncomeForm()
    budget_form = BudgetForm()

    expenses = Expense.objects.filter(
        user=request.user, date__year=year, date__month=month
    ).order_by("-date")

    category_filter = request.GET.get("category")
    filtered_expenses = expenses.filter(
        category__iexact=category_filter
    ) if category_filter else expenses

    incomes = Income.objects.filter(
        user=request.user, date__year=year, date__month=month
    ).order_by("-date")

    source_filter = request.GET.get("source")
    filtered_incomes = incomes.filter(
        source__iexact=source_filter
    ) if source_filter else incomes

    budgets = Budget.objects.filter(
        user=request.user, month__year=year, month__month=month
    ).order_by("-month")

    total_expenses = expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0")
    total_income = incomes.aggregate(total=Sum("amount"))["total"] or Decimal("0")
    total_budget = budgets.aggregate(total=Sum("amount"))["total"] or Decimal("0")
    balance = total_income - total_expenses

    category_data = (
        expenses.values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    budget_data = []
    for budget in budgets:
        spent = (
            expenses.filter(category__iexact=budget.category)
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
        )
        remaining = budget.amount - spent
        percentage = (spent / budget.amount) * 100 if budget.amount > 0 else 0
        display_percentage = min(percentage, 100)
        status = "Within Budget" if remaining >= 0 else "Over Budget"

        budget_data.append({
            "budget": budget,
            "spent": spent,
            "remaining": remaining,
            "status": status,
            "percentage": display_percentage,
        })

    return render(request, "expenses/home.html", {
        "expense_form": expense_form,
        "income_form": income_form,
        "budget_form": budget_form,
        "filtered_expenses": filtered_expenses,
        "filtered_incomes": filtered_incomes,
        "budgets": budgets,
        "category_filter": category_filter,
        "source_filter": source_filter,
        "budget_data": budget_data,
        "category_data": category_data,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "total_budget": total_budget,
        "year": year,
        "month": month,
    })


@login_required
def delete_expense(request, expense_id):
    user_expense(request, id=expense_id).delete()
    return redirect("home")


@login_required
def delete_income(request, income_id):
    user_income(request, id=income_id).delete()
    return redirect("home")


@login_required
def edit_expense(request, expense_id):
    expense = user_expense(request, id=expense_id)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ExpenseForm(instance=expense)

    return render(request, "expenses/edit_expense.html", {"form": form, "expense": expense})


@login_required
def edit_income(request, income_id):
    income = user_income(request, id=income_id)

    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = IncomeForm(instance=income)

    return render(request, "expenses/edit_income.html", {"form": form, "income": income})


@login_required
def edit_budget(request, budget_id):
    budget = user_budget(request, id=budget_id)

    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = BudgetForm(instance=budget)

    return render(request, "expenses/edit_budget.html", {"form": form, "budget": budget})


@login_required
def delete_budget(request, budget_id):
    user_budget(request, id=budget_id).delete()
    return redirect("home")
