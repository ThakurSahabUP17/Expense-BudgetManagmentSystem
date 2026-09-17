from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("delete-expense/<int:expense_id>/", views.delete_expense, name="delete_expense"),
    path("delete-income/<int:income_id>/", views.delete_income, name="delete_income"),
    path("edit-expense/<int:expense_id>/", views.edit_expense, name="edit_expense"),
    path("edit-income/<int:income_id>/", views.edit_income, name="edit_income"),
    path("edit-budget/<int:budget_id>/", views.edit_budget, name="edit_budget"),
    path("delete-budget/<int:budget_id>/", views.delete_budget, name="delete_budget"),
]
