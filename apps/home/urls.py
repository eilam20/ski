# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.home import views
from apps.home.views import CreateOrder, update_order_complete

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("create_order/", CreateOrder.as_view(), name='order-create'),
    path("edit_order/<int:pk>", CreateOrder.as_view(), name='order-edit'),
    path("done_order/<int:pk>", update_order_complete, name='order-done'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
