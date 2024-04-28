from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(ListCreateAPIView):

    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product) 
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'Error': 'This product can not be deleted. it is associated with order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class CollectionList(ListCreateAPIView):

    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
    collection = get_object_or_404(Collection.objects.annotate(
        products_count=Count('products')),
        pk=id
    )
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({
                'Error': 'This collection can not be deleted. it is associated with some products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)