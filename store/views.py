from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order
# Create your views here.




def index(request):
    # Récupérer tous les produits pour afficher les options dans le datalist
    products = Product.objects.all()
    product = None  # Variable pour stocker le produit trouvé (via le formulaire de recherche)

    # Vérifier si une recherche a été effectuée via le formulaire
    if request.method == 'POST':
        search_slug = request.POST.get('product_slug')
        if search_slug:
            product = Product.objects.filter(slug=search_slug).first()

    # Gérer le tri des produits
    sort_by = request.GET.get('sort_by')
    if sort_by == "price_asc":
        products = products.order_by("price")  # Prix croissant
    elif sort_by == "price_desc":
        products = products.order_by("-price")  # Prix décroissant
    elif sort_by == "rating_asc":
        products = products.order_by("rating")  # Rating croissant
    elif sort_by == "rating_desc":
        products = products.order_by("-rating")  # Rating décroissant

    return render(request, 'store/index.html', {'products': products, 'product': product, 'sort_by': sort_by})



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

    return render(request, 'store/cart.html', context={"orders" : cart.orders.all()})


def delete_cart(request):
    cart = request.user.cart
    orders = request.user.cart.orders.all()

    if cart:
        # Supprimer toutes les commandes associées au panier
        orders.delete()
        # Supprimer le panier
        cart.delete()

    return redirect('index')


def page_user(request):
    ordered_orders = Order.objects.filter(user=request.user, ordered=True)
    return render(request, 'store/user_page.html', context={"orders": ordered_orders})

def valid_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    orders = cart.orders.filter(ordered=False)

    for order in orders:
        order.ordered = True
        order.save()

    cart.orders.clear()
    return redirect('index')