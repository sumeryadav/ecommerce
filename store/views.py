
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product


@login_required(login_url='login')
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'quantity': 1
        }

    request.session['cart'] = cart
    return redirect('cart')

def increase_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'quantity': 1
        }

    request.session['cart'] = cart
    return redirect('cart')



def decrease_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id]['quantity'] > 1:
            cart[product_id]['quantity'] -= 1
        else:
            del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')



def cart(request):
    cart = request.session.get('cart', {})  # cart stored in session

    cart_items = []
    total = 0

    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=product_id)

        # Get quantity depending on how you store cart
        # If cart stores dict like {"quantity": 2, "price": 299.99}
        quantity = item_data.get('quantity', 1)

        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total
        })

    context = {
        'cart_items': cart_items,
        'total': total
    }

    return render(request, 'cart.html', context)


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')

def search(request):
    query = request.GET.get('q', '')
    return render(request, 'store/search.html', {
        'query': query
    })