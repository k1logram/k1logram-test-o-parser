from django.shortcuts import render
from rest_framework import generics, status

from .serializers import ProductSerializer
from .models import Product

from .tasks import parse_product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


# Create your views here.

class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    def get(self, request):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        return Response(serializer_class(queryset, many=True).data)

    def post(self, request):
        data = request.data
        if 'products_count' in list(data.keys()):
            products_count = data['products_count']
        else:
            products_count = 10

        if products_count < 1 or products_count > 50:
            return Response(data={'msg': 'products_count должен быть от 1 до 50'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            parse_product.delay(products_count)
            return Response(data={'msg': 'Задача по парсингу добавлена в очередь'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_product(request, product_id):
    if product_id < 1:
        return Response(data={'msg': 'product_id должен быть больше нуля'})
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(data={'msg': 'Не существует продукта с таким ID'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)

    response = Response(serializer.data)
    response.accepted_renderer = JSONRenderer()

    return response




