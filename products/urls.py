from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('products/<str:typeof>', views.showProducts, name="products"),
    path('product/<str:pk>', views.showSingleProduct, name="single-product"),
    path('show-products-cart/', views.showProductsCart, name="show-products-cart"),
    path('', views.showHomePage, name="home"),
    path('products_search/', views.productsSearch, name="products-search"),
    path('products_sort/<str:typeof>', views.productsSort, name="products-sort"),
    path('download_bill/', views.downloadBill, name="download-bill"),
    path('prepare_bill/', views.prepareBill, name="prepare-bill"),

    url(r'^getProductsFromJS$', views.getProductsFromJS,
        name='getProductsFromJS'),
    url(r'^deleteProductsFromJS$', views.deleteProductsFromJS,
        name='deleteProductsFromJS'),
]
