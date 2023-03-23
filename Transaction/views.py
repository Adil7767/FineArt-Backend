from django.db.models import Sum
from rest_framework import viewsets, status
from Transaction.serializers import *
from account.renderers import UserRenderer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.http import JsonResponse
from Transaction.filters import Filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from Transaction.pagination import Add_TransactionPagination


# Create your views here.
class TypeView(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminUser]


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminUser]


class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminUser]


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

    def create(self, request):
        serializer = TotalTransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            trans_type = serializer.data.get('trans_type')
            data = Add_Transaction.objects.filter(type=trans_type).aggregate(Sum('amount'))
            if Type.objects.filter(id=trans_type).exists():
                type_name = Type.objects.get(id=trans_type)
                return JsonResponse({type_name.add_type: data}, status=status.HTTP_200_OK)
        return Response({'error': "Transaction doesn't exist."}, status=status.HTTP_403_FORBIDDEN)

