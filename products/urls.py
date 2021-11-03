from django.urls import path
from . import views


urlpatterns = [
    path('products/<str:type>', views.showProducts, name="products"),
    path('product/<str:pk>', views.showSingleProduct, name="single-product"),

]
