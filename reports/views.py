from django.db.models import Sum, Count
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from billing.models import Bill, BillItem


class TodaySalesReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        today = now().date()

        bills = Bill.objects.filter(created_at__date=today)

        total_sales = bills.aggregate(total=Sum('total_amount'))['total'] or 0
        total_bills = bills.count()

        cash_total = bills.filter(payment_method='CASH').aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        upi_total = bills.filter(payment_method='UPI').aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        return Response({
            "date": str(today),
            "total_sales": total_sales,
            "total_bills": total_bills,
            "cash_sales": cash_total,
            "upi_sales": upi_total
        })


class DateRangeSalesReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        from_date = request.GET.get('from')
        to_date = request.GET.get('to')

        if not from_date or not to_date:
            return Response(
                {"detail": "from and to dates are required"},
                status=400
            )

        bills = Bill.objects.filter(
            created_at__date__range=[from_date, to_date]
        )

        total_sales = bills.aggregate(total=Sum('total_amount'))['total'] or 0
        total_bills = bills.count()

        return Response({
            "from": from_date,
            "to": to_date,
            "total_sales": total_sales,
            "total_bills": total_bills
        })


class ItemWiseSalesReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response(status=status.HTTP_403_FORBIDDEN)

        items = (
            BillItem.objects
            .values('product__name')
            .annotate(
                total_quantity=Sum('quantity'),
                total_amount=Sum('price')
            )
            .order_by('-total_quantity')
        )

        return Response(items)