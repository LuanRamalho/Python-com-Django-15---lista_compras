from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_notas, name='lista_notas'),
    path('criar/', views.criar_nota, name='criar_nota'),
    path('nota/<int:nota_id>/', views.visualizar_nota, name='visualizar_nota'),
    path('nota/<int:nota_id>/editar/', views.editar_nota, name='editar_nota'),
    path('nota/<int:nota_id>/excluir/', views.excluir_nota, name='excluir_nota'),
    path('nota/<int:nota_id>/adicionar/', views.adicionar_item, name='adicionar_item'),
    path('item/<int:item_id>/editar/', views.editar_item, name='editar_item'),
    path('item/<int:item_id>/excluir/', views.excluir_item, name='excluir_item'),
]
