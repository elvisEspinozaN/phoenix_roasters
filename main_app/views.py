from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UpdateForm, SignupForm
from .forms import *
from .models import *
import datetime


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {
        'products': products
    })

def about(request):
    return render(request, 'about.html')

def contactus(request):
    return render(request, 'contactus.html')

def location(request):
    return render(request, 'location.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username')
            raw_password = signup_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(
                request, "You have successfully created an account!")
            login(request, user)
            return redirect('home')
    else:
        signup_form = SignupForm()
    return render(request, 'registration/signup.html', context={"signup_form": signup_form})

def shoppingcarts_index(request):
    if request.user.is_authenticated:
        user=request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        products = order.cartorder_set.all()
    else:
        products = []
    context = {'products': products}
    return render(request, 'shoppingcarts/index.html', context)

@login_required
def shoppingcarts_add(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    quantity = request.POST.get('quantity')
    order = Order.objects.get(user=request.user)
    cartorder = CartOrder(order=order, product=product, quantity=quantity)
    cartorder.save()
    return redirect('shoppingcarts_index')

def shoppingcarts_delete(request, id):
    CartOrder.objects.filter(id=id).delete()
    messages.success(request, 'Your item has been delete')
    return HttpResponseRedirect('/shoppingcarts')


def products_index(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'products/index.html', {
        'products': products
    })

def products_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/detail.html', {
        'product': product,
    })

@login_required()


def checkouts_index(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)

        if order_form.is_valid:
            order = order_form.save(commit=False)
            order.user = request.user
            order.date = datetime.now()
            order.save()

            shoppingcart = request.session.get('shoppingcarts_index', {})
            total = 0
            for id, quantity in shoppingcart.items():
                product = get_object_or_404(Product, pk=id)
                total += quantity * product.price
                cart_order = CartOrder(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
                cart_order.save()

def search_view(request):
    products = Product.objects.filter(name__icontains=request.GET['q'])
    if products.exists():
        return render(request, 'products/index.html', {'products': products})
    else:
        search_query = request.GET['q']
        products = Product.objects.all()
        return render(request, 'search/none.html', {'products': products, 'search_query': search_query})


""""""""""""""""""""""""""

class ProductCreate(CreateView):
    pass

class ProductUpdate(UpdateView):
    pass

class ProductDelete(DeleteView):
    pass
class IndexView(ListView):
    template_name = 'shoppingcarts/index.html'
    context_object_name = 'product'
    queryset = Product.objects.all().prefetch_related('shoppingcarts_set.all')