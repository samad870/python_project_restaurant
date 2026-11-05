"""
urls.py - URL routing for the management app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Customer Management
    path('customers/', views.customer_list_view, name='customer_list'),
    path('customers/<str:customer_id>/delete/', views.customer_delete_view, name='customer_delete'),

    # Menu Management
    path('menu/', views.menu_list_view, name='menu_list'),
    path('menu/<str:item_id>/delete/', views.menu_delete_view, name='menu_delete'),

    # Order Management
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/create/', views.order_create_view, name='order_create'),
    path('orders/<str:order_id>/', views.order_details_view, name='order_details'),
    path('orders/<str:order_id>/status/', views.order_status_update_view, name='order_status_update'),

    # Billing Management
    path('billing/', views.billing_view, name='billing'),
    path('billing/<str:order_id>/', views.billing_view, name='billing_order'),
]

