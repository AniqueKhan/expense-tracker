from django.urls import path
from expenses.views import *

urlpatterns = [
    path("", index, name='index'),
    path("add-expense", add_expense, name='add_expense'),
]
