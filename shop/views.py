from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q

from .forms import CheckoutForm
from .models import Book, Cart, CartItem, Order, OrderItem

def books_list(request):
    query = request.GET.get('q')
    #Filters books by title or author
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'shop/book_list.html', {'books': books})

def book_detail(request, book_id):
    #Displays extra detail for each book
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'shop/book_detail.html', {'book': book})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id= book_id)

    #Gets or creates a cart for user
    cart, created = Cart.objects.get_or_create(user=request.user)

    #Gets or creates a cart item for selected book
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity+=1
    cart_item.save()

    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/view_cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('view_cart')

@require_POST
def update_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity is zero
    except ValueError:
        pass  # Ignore invalid input
    return redirect('view_cart')

from django.db import transaction

@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
            # Use a database transaction to ensure atomicity

                order = Order.objects.create(
                    user=request.user,
                    full_name=form.cleaned_data['full_name'],
                    email=form.cleaned_data['email'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    postal_code=form.cleaned_data['postal_code'],
                    paid=True
                )

                # Create corresponding OrderItems from cart items
                for item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        book=item.book,
                        price=item.book.price,
                        quantity=item.quantity
                    )
                    
                # Clear cart after order is placed
                cart.items.all().delete()
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'shop/checkout.html', {'form': form, 'cart': cart})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/confirmation.html', {'order': order})

def help_view(request):
    return render(request, 'shop/help.html')