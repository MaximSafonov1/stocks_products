from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # фильтрация
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    # # фильтрация
    # filter_backends = [DjangoFilterBackend]
    # filter_fields = ['products']

    # поиск по id, title или description продукта
    def get_queryset(self):
        param = self.request.GET.get('products', None)

        if param is None:
            queryset = Stock.objects.all()
        else:
            if param.isdigit():
                queryset = Stock.objects.filter(products=param)
            else:
                queryset = Stock.objects.filter(Q(products__title__icontains=param) |
                                                Q(products__description__icontains=param))
        return queryset
