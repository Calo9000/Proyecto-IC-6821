from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .interface import ITransaccional
from .singleton import SingletonMeta
from .controllers import Controladora

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


controladora = Controladora()

@unauthenticated_user
def registerPage(request):
    return controladora.registerPage(request)

@unauthenticated_user
def loginPage(request):
    return controladora.loginPage(request)

def logoutUser(request):
    return controladora.logoutUser(request)

@login_required(login_url='login')
@admin_only
def home(request):
    return controladora.home(request)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    return controladora.userPage(request)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    return controladora.accountSettings(request)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    return controladora.products(request)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    return customer(request, pk_test) 

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    return controladora.createOrder(request, pk)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    return controladora.updateOrder(request, pk)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    return controladora.deleteOrder(request, pk)




