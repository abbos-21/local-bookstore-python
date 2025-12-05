from .views import _get_cart, CART_SESSION_ID

def cart_total(request):
    cart = request.session.get(CART_SESSION_ID, {})
    total_qty = sum(item.get('quantity', 0) for item in cart.values())
    return {'cart_total_qty': total_qty}
