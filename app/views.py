from email import message
from functools import total_ordering
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
#from .models import *
from app import models
from .forms import OrderForm, UserForm, CustomerForm
from .filters import OrderFilter
from .decorators import allowed_users, unauthenticated_user, admin_only


@unauthenticated_user
def register_page(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
        

    context = {'form':form}
    return render(request, 'register.html', context)

@unauthenticated_user        
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()
    
    print('ORDERS:',orders)
    context = {'orders':orders, 'total_orders':total_orders,
    'delivered':delivered, 'pending':pending}
    return render(request, 'user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'account_settings.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
    orders = models.Order.objects.all()
    customers = models.Customer.objects.all()

    total_orders = orders.count()
    total_customers = customers.count()

    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()

    context = {'orders':orders, 'customers':customers, 
    'total_orders':total_orders, 'total_customers':total_customers,
    'delivered':delivered, 'pending':pending}
    return render(request, 'dashboard.html', context)
   
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = models.Customer.objects.get(id=pk)
    order = customer.order_set.all()
    order_count = order.count()

    myFilter = OrderFilter(request.GET, queryset=order)
    order = myFilter.qs

    context = {'customer':customer, 'order':order, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    p = models.Product.objects.all()
    #products = Product.objects.all()
    return render(request, 'products.html', {"product":p})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    customer = models.Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'form':form}
    return render(request, 'order_form.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = models.Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'form':form}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = models.Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    
    context = {'item':order}
    return render(request, 'delete.html', context)