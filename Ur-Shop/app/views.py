from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.views.generic import CreateView

from .forms import *
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


def buy_now(request):
    return render(request, 'app/buynow.html')


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


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']

            new_address = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode, )
            new_address.save()
            messages.success(request, 'Address updated successful.')

        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


def address(request):
    address = Customer.objects.filter(user=request.user)
    # print(address)
    return render(request, 'app/address.html', {'add': address, 'active': 'btn-primary'})


def edit_address(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        fm = CustomerProfileForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()

    else:
        pi = Customer.objects.get(pk=id)
        fm = CustomerProfileForm(request.POST, instance=pi)
        address = Customer.objects.filter(user=request.user)
        print(address)

        return render(request, 'app/edit_address.html', {'form': fm, 'add': address})

    return HttpResponseRedirect('/address/')


def delete_address(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        pi.delete()
    return HttpResponseRedirect('/address/')


def add_to_cart(request):
    usr = request.user
    product_id = request.GET.get('prod_id')
    # print('id', product_id)
    product = Product.objects.get(pk=product_id)
    # print('instance', product)
    Cart(user=usr, product=product).save()

    return redirect('/cart')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user)
        # print(carts)
        cart_product = [p for p in carts]
        # print(cart_product)

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        # Cart.objects.all() এ সকল ইউজারের কার্ট পাওয়া যাবে; তো এখানে সমস্ত ইউজরের প্রথম প্রোডাক্ট বের করে 'p' তে
        # রাখা হবে এবং চেক করে হবে যে p.user মানে এই প্রোডাক্টের ইউজার আর বর্তমানে যে ইউজার লগইন করে আছে মানে
        # request.user একই ইউজার কিনা, যদি এক হয় তাহলে [p for ... এই p  তে রাখা হবে।
        # cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
                total_amount = amount + shipping_amount
                print(p)

            return render(request, 'app/addtocart.html',
                          {'carts': carts, 'amount': amount, 'total_amount': total_amount})

        else:
            return render(request, 'app/empty_cart.html')


def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        print(prod_id)
        current = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # print(current)

        current.quantity += 1
        current.save()
        print(current.quantity)

        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0

        # Cart.objects.all() এ সকল ইউজারের কার্ট পাওয়া যাবে; তো এখানে সমস্ত ইউজরের প্রথম প্রোডাক্ট বের করে 'p' তে
        # রাখা হবে এবং চেক করে হবে যে p.user মানে এই প্রোডাক্টের ইউজার আর বর্তমানে যে ইউজার লগইন করে আছে মানে
        # request.user একই ইউজার কিনা, যদি এক হয় তাহলে [p for ... এই p  তে রাখা হবে।
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        # print(cart_product)

        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
            totalamount = amount + shipping_amount

        data = {
            'quantity': current.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    return render(request, 'app/addtocart.html',
                          )


def minus_cart(request):
    pass
