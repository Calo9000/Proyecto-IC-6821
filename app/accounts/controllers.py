from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .interface import ITransaccional
from . singleton import SingletonMeta

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

class GestorDeOrdenes(ITransaccional):

    def create(self,POST, pk):
        
        customer = Customer.objects.get(id=pk)

        #form = OrderForm(initial={'customer':customer})

        #print('Printing POST:', request.POST)
        form = OrderForm(POST)
        formset = OrderFormSet(POST, instance=customer)
        if formset.is_valid():
            formset.save()





    def update(self,POST, pk):
        order = Order.objects.get(id=pk)

        print('ORDER:', order)

        form = OrderForm(POST, instance=order)
        if form.is_valid():
            form.save()

    def get(self,POST,pk):
        pass




    def delete(self,POST, pk):
        order = Order.objects.get(id=pk)

        order.delete()

class Controladora(metaclass=SingletonMeta):
    gestorDeOrdenes = GestorDeOrdenes()


    def registerPage(self,request):

        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')


                messages.success(request, 'Account was created for ' + username)

                return redirect('login')
            

        context = {'form':form}
        return render(request, 'accounts/register.html', context)


    def loginPage(self,request):

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
        return render(request, 'accounts/login.html', context)

    def logoutUser(self,request):
        logout(request)
        return redirect('login')

    def home(self,request):
        orders = Order.objects.all()
        customers = Customer.objects.all()

        total_customers = customers.count()

        total_orders = orders.count()
        delivered = orders.filter(status='Delivered').count()
        pending = orders.filter(status='Pending').count()

        context = {'orders':orders, 'customers':customers,
        'total_orders':total_orders,'delivered':delivered,
        'pending':pending }

        return render(request, 'accounts/dashboard.html', context)


    def userPage(self,request):
        orders = request.user.customer.order_set.all()

        total_orders = orders.count()
        delivered = orders.filter(status='Delivered').count()
        pending = orders.filter(status='Pending').count()

        print('ORDERS:', orders)

        context = {'orders':orders, 'total_orders':total_orders,
        'delivered':delivered,'pending':pending}
        return render(request, 'accounts/user.html', context)


    def accountSettings(self,request):
        customer = request.user.customer
        form = CustomerForm(instance=customer)

        if request.method == 'POST':
            form = CustomerForm(request.POST, request.FILES,instance=customer)
            if form.is_valid():
                form.save()


        context = {'form':form}
        return render(request, 'accounts/account_settings.html', context)





    def products(self,request):
        products = Product.objects.all()

        return render(request, 'accounts/products.html', {'products':products})


    def customer(self,request, pk_test):
        customer = Customer.objects.get(id=pk_test)

        orders = customer.order_set.all()
        order_count = orders.count()

        myFilter = OrderFilter(request.GET, queryset=orders)
        orders = myFilter.qs 

        context = {'customer':customer, 'orders':orders, 'order_count':order_count,
        'myFilter':myFilter}
        return render(request, 'accounts/customer.html',context)


    def createOrder(self,request, pk):
        OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
        customer = Customer.objects.get(id=pk)
        formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
        #form = OrderForm(initial={'customer':customer})
        if request.method == 'POST':
            #print('Printing POST:', request.POST)
            self.gestorDeOrdenes.create(request.POST,pk)
            return redirect('/')

        context = {'form':formset}
        return render(request, 'accounts/order_form.html', context)


    def updateOrder(self,request, pk):
        order = Order.objects.get(id=pk)
        form = OrderForm(instance=order)
        print('ORDER:', order)
        if request.method == 'POST':

            self.gestorDeOrdenes.update(request.POST,pk)
            return redirect('/')

        context = {'form':form}
        return render(request, 'accounts/order_form.html', context)


    def deleteOrder(self,request, pk):
        order = Order.objects.get(id=pk)
        if request.method == "POST":
            self.gestorDeOrdenes.delete(request.POST,pk)
            return redirect('/')

        context = {'item':order}
        return render(request, 'accounts/delete.html', context)