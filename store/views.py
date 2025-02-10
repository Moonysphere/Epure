from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order
from django.db.models import Sum
# Create your views here.




def index(request):
    # Récupérer tous les produits pour afficher les options dans le datalist
    products = Product.objects.all()

    # Initialiser la variable pour afficher le produit trouvé
    product = None

    # Vérifier si un formulaire a été soumis
    if request.method == 'POST':
        search_slug = request.POST.get('product_slug')
        if search_slug:
            product = Product.objects.filter(slug=search_slug).first() 
    
    return render(request, 'store/index.html', {'products': products, 'product': product})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={"product": product})

def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, product=product, ordered = False)
    

    if created:
        cart.orders.add(order)
        cart.save()
    else: 
        order.quantity += 1
        order.save()

    return redirect(reverse("product", kwargs={"slug" : slug}))

def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_quantity = cart.orders.aggregate(Sum('quantity'))['quantity__sum'] or 0

    return render(request, 'store/cart.html', context={"orders": cart.orders.all(), "total_quantity": total_quantity})

def delete_cart(request):
    cart = request.user.cart
    orders = request.user.cart.orders.all()

    if cart:
        # Supprimer toutes les commandes associées au panier
        orders.delete()
        # Supprimer le panier
        cart.delete()

    return redirect('index')


