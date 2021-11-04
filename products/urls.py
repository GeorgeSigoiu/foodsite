from django.conf.urls import url
from django.http.response import JsonResponse
from django.urls import path
from . import views


urlpatterns = [
    path('products/<str:type>', views.showProducts, name="products"),
    path('product/<str:pk>', views.showSingleProduct, name="single-product"),
    path('show-products-cart/', views.showProductsCart, name="show-products-cart"),
    path('', views.showHomePage, name="home"),
    path('location/<str:map_string>/', views.openLocationOnMaps, name="location"),
    path('products_search/', views.productsSearch, name="products-search"),

    url(r'^transferBetweenDJandJS$', views.transferBetweenDJandJS,
        name='transferBetweenDJandJS'),
]
