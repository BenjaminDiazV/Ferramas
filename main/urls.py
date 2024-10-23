from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('catalogo', views.catalogo, name='catalogo'),
    path('inventario', views.inventario, name='inventario'),
    path("prod_add", views.prod_add, name = "prod_add"),
    path("prod_del/<str:pk>", views.prod_del, name = "prod_del"),
    path("prod_findEdit/<str:pk>", views.prod_findEdit, name = "prod_findEdit"),
    path("producto_edit", views.producto_edit, name = "producto_edit"),
]
