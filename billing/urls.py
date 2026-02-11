from django.urls import path

from .views import (
    CreateBillView,
    BillListView,
    BillDetailView,
)

urlpatterns = [
    # 🔥 Create bill (POS payment)
    path("bills/", CreateBillView.as_view()),

    # 📜 Bill history (list + filters)
    path("bills/history/", BillListView.as_view()),

    # 🧾 Bill detail (view / reprint)
    path("bills/<int:pk>/", BillDetailView.as_view()),
]
