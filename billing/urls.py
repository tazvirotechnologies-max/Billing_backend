from django.urls import path
from .views import CreateBillView

urlpatterns = [
    path('bills/', CreateBillView.as_view()),
]