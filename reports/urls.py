from django.urls import path
from .views import (
    TodaySalesReport,
    DateRangeSalesReport,
    ItemWiseSalesReport
)

urlpatterns = [
    path('reports/today/', TodaySalesReport.as_view()),
    path('reports/date-range/', DateRangeSalesReport.as_view()),
    path('reports/items/', ItemWiseSalesReport.as_view()),
]