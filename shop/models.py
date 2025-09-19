from django.db import models
from django.contrib.auth.models import User

"""
This module defines the core models for the shop application:
- Book: Represents books for sale.
- Cart & CartItem: Represent a user's shopping cart and its contents.
- Order & OrderItem: Represent a completed purchase and its details.
"""


class Book(models.Model):
    # Book information
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)#
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Cart(models.Model):
    #One cart per user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
class CartItem(models.Model):
    #links each item to a cart and a book
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} (x{self.quantity})"
    
    def total_price(self):
        return self.book.price * self.quantity
    

class Order(models.Model):
    #customer details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
class OrderItem(models.Model):

    # Each item belongs to an order and refers to a book
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def get_cost(self):
        return self.price * self.quantity
