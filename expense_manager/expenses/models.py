from django.conf import settings
from django.db import models


class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Travel", "Travel"),
        ("Education", "Education"),
        ("Shopping", "Shopping"),
        ("Bills", "Bills"),
        ("Entertainment", "Entertainment"),
        ("Health", "Health"),
        ("Other", "Other"),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - ₹{self.amount}"


class Income(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    SOURCE_CHOICES = [
        ("Salary", "Salary"),
        ("Pocket Money", "Pocket Money"),
        ("Scholarship", "Scholarship"),
        ("Freelance", "Freelance"),
        ("Business", "Business"),
        ("Other", "Other"),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.source} - ₹{self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()

    def __str__(self):
        return f"{self.category} - ₹{self.amount}"
