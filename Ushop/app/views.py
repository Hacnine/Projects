from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.views.generic import CreateView

from .forms import CustomerRegistrationForm, MyPasswordChangeForm
from .models import *


# def home(request):
#     return render(request, 'app/home.html')


class ProductView(View):

    def get(self, request):
        top_wears = Product.objects.filter(category='TW')
        bottom_wears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html',
                      {'topwears': top_wears, 'bottomwears': bottom_wears, 'mobiles': mobiles})


# def product_detail(request):
#     return render(request, 'app/productdetail.html')

class ProductDetailView(View):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})


def add_to_cart(request):
    return render(request, 'app/addtocart.html')


def buy_now(request):
    return render(request, 'app/buynow.html')


def profile(request):
    return render(request, 'app/profile.html')


def address(request):
    return render(request, 'app/address.html')


def orders(request):
    return render(request, 'app/orders.html')


# def change_password(request):
#     return render(request, 'app/changepassword.html')


def mobile(request, data=None):
    mobiles = None
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Oppo' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
        # return mobiles
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=9500)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=9500)

    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def login(request):
    return render(request, 'app/login.html')


# def customerregistration(request):
#     return render(request, 'app/registrationform.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/registrationform.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Registered Successful.')
            form.save()
        return render(request, 'app/registrationform.html', {'form': form})


def checkout(request):
    return render(request, 'app/checkout.html')

