from django.shortcuts import render
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from django.db.models import Model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import AccountAuthenticationForm, RegistrationForm
from .models import Account, MyAccountManager

# Import outside of Python and Django
from web3 import Web3

# Create your views here.


def register_page(request):
    form = RegistrationForm()
    context = {}
    if request.method == "GET":
        context['form'] = form
        return render(request, "templates/register_page.html", context)

    elif request.method == "POST":
        form = RegistrationForm(request.POST)
        if form is not None:
            user = form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect("home")

def home(request):
    user = request.user
    print(user)
    context = {}
    context['user'] = user
    if request.method == "GET":
        return render(request, "templates/home.html", context)

def login_page(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form is not None:
            email = form.data['email']
            password = form.data['password']
            user = authenticate(email=email, password=password)
            print(user)

            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    context["login_form"] = form
    return render(request, "templates/login_page.html", context)


def logout_page(request):
    logout(request=request)
    return redirect('login_page')


def deposit_eth(request):
    context = {}
    user = request.user
    context['user'] = user
    if request.method == "GET":

        return render(request, "templates/deposit_eth.html", context)

    if request.method == "POST":
        eth_send = request.POST.get("eth_send")
        eth_send = float(eth_send)
        user_eth_before_tx = user.eth
        user_eth_before_tx = float(user_eth_before_tx)
        user_coins_after_tx = user_eth_before_tx + eth_send
        user.eth = str(user_coins_after_tx)
        user.save() 
        context = {}
        context['eth_send'] = eth_send

        return HttpResponse(json.dumps(context), content_type="application/json")

def withdraw_eth(request):
    
    user = request.user
    context = {}
    context["user"] = user

    if request.method == "GET":
        return render(request, "templates/withdraw_eth.html", context)
    
    if request.method == "POST":
        eth_withdraw = request.POST.get("eth_withdraw")
        wallet_address = request.POST.get("wallet_address")
        eth_withdraw = float(eth_withdraw)
        user_eth_before_tx = user.eth
        user_eth_before_tx = float(user_eth_before_tx)
        if user_eth_before_tx  >= eth_withdraw: 

            user_eth_after_tx = user_eth_before_tx - eth_withdraw
            user.eth = user_eth_after_tx
            user.save()

            w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/428a3a63ef3c4b0c8750d7952c1e6ea4"))
            my_address = Web3.toChecksumAddress("my_public_address")
            user_address = Web3.toChecksumAddress(wallet_address)
            private_key = "My Private Key Goes Here"

            nonce = w3.eth.getTransactionCount(my_address)

            tx = {
                "nonce": nonce,
                "to": user_address,
                "value": w3.toWei(0.001, "ether"),
                "gas": 21000,
                "gasPrice": w3.toWei(40, "gwei"),
            }

            signed_tx = w3.eth.account.sign_transaction(tx, private_key)

            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)





        return HttpResponse(json.dumps(context), content_type="application/json")


