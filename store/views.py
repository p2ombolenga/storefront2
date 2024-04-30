from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .filters import ProductFilter

class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

     
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({
                'Error': 'Product can not be deleted. it is associated with One or more order items'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
        return super().destroy(request, *args, **kwargs) 

class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer  

    def destroy(self, request, *args, **kwargs):
          if Product.objects.filter(collection=kwargs['pk']).count() > 0:
              return Response({
                'Error': 'This collection can not be deleted. it is associated with some products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
          return super().destroy(request, *args, **kwargs)
    

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer


    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}        