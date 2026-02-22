from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from Transaction.serializers import *
from Transaction.models import Add_Transaction, Type, Category, Payment
from account.renderers import UserRenderer
from Transaction.filters import Filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from Transaction.pagination import Add_TransactionPagination


# Create your views here.
class _TypeCategoryPaymentMixin:
    """Allow any authenticated user to list/retrieve; admin only for create/update/delete."""
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsAdminUser()]


class TypeView(_TypeCategoryPaymentMixin, viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]


class CategoryView(_TypeCategoryPaymentMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]


class PaymentView(_TypeCategoryPaymentMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]


class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    renderer_classes = [UserRenderer]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = Filter
    search_fields = ['description']
    pagination_class = Add_TransactionPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            return Add_Transaction.objects.all()
        else:
            return Add_Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, pk=None):
        try:
            transaction = Add_Transaction.objects.get(pk=pk)
        except Add_Transaction.DoesNotExist:
            return Response({'error': 'Transaction does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff and transaction.user != request.user:
            return Response({'error': 'You do not have permission to update this transaction'}, status=status.HTTP_403_FORBIDDEN)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            transaction = Add_Transaction.objects.get(pk=pk)
        except Add_Transaction.DoesNotExist:
            return Response({'error': 'Transaction does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_staff and transaction.user != request.user:
            return Response({'error': 'You do not have permission to delete this transaction'}, status=status.HTTP_403_FORBIDDEN)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TotalTransactionView(viewsets.ModelViewSet):
    serializer_class = TotalTransactionSerializer
    http_method_names = ['post']
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = TotalTransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            trans_type = serializer.validated_data.get('trans_type')
            qs = Add_Transaction.objects.filter(type=trans_type)
            if not request.user.is_staff:
                qs = qs.filter(user=request.user)
            data = qs.aggregate(Sum('amount'))
            amount_sum = float(data.get('amount__sum') or 0)
            if Type.objects.filter(id=trans_type).exists():
                type_obj = Type.objects.get(id=trans_type)
                return Response({
                    'data': {'amount__sum': amount_sum},
                    'type_name': type_obj.add_type,
                }, status=status.HTTP_200_OK)
        return Response({'error': "Transaction doesn't exist."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chart_stats_view(request):
    """GET: returns line (monthly totals) and pie (category breakdown) for charts. Requires auth."""
    from collections import OrderedDict
    from decimal import Decimal
    qs = Add_Transaction.objects.filter(user=request.user)
    # Last 6 months by month
    six_months_ago = timezone.now() - timezone.timedelta(days=180)
    monthly = (
        qs.filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    months = []
    totals = []
    for m in monthly:
        months.append(m['month'].strftime('%b') if m['month'] else '')
        totals.append(float(m['total'] or 0))
    # If no data, use placeholder
    if not months:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        totals = [0, 0, 0, 0, 0, 0]
    line = {'labels': months, 'datasets': [{'data': totals}]}
    # Pie: by category
    cat_totals = (
        qs.values('category__new_category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    colors = ['#5B39CB', '#17cf97', '#f74871', '#ffbc47', '#194ad1', '#b81ff0']
    pie = []
    for i, c in enumerate(cat_totals):
        name = c['category__new_category'] or 'Other'
        pie.append({
            'name': name,
            'population': float(c['total'] or 0),
            'color': colors[i % len(colors)],
            'legendFontColor': '#333',
            'legendFontSize': 12,
        })
    if not pie:
        pie = [
            {'name': 'No data', 'population': 1, 'color': '#eee', 'legendFontColor': '#333', 'legendFontSize': 12}
        ]
    return Response({'line': line, 'pie': pie})

