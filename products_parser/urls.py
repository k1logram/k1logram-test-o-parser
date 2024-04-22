from django.urls import path
from .views import ProductView, get_product

app_name = 'products_parser'

urlpatterns = [
    path('v1/products/', ProductView.as_view()),
    path('v1/products/<int:product_id>/', get_product, name='product'),
]
