from django.urls import path
from . import views

urlpatterns = [
    #Book-related views
    path('', views.books_list, name='books_list'),
    path ('books/<int:book_id>/', views.book_detail, name='book_detail'),

    #Cart-related views
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),

    #Checkout-related views
    path('checkout/', views.checkout_view, name='checkout'), 
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

    #Help-related views
    path('help/', views.help_view, name='help'),
]