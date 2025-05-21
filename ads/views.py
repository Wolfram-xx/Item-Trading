from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from django.contrib.auth import *
from django.contrib.auth.models import User
from ads.models import *

# Create your views here.
def index_page(request):
    return render(request, "index.html")

def reg(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_2 = request.POST.get("password_again")
        if password_2 != password:
            return redirect('/error_auth/')                                          # Write
        # Логика обработки пользователя
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_me(request)
            return redirect('/profile/')
        else:
            return redirect('/error_auth/')

def error_auth(request):
    return render(request, "auth_error.html")

def login_me(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile/')
        else:
            return redirect('/error_auth/')

def profile_page(request):
    if request.user.is_authenticated:
        search_text = request.GET.get('search', '')
        category = request.GET.get('category', '')
        condition = request.GET.get('condition', '')
        query = Q(title__icontains=search_text) | Q(description__icontains=search_text)
        if category:
            cat_query = Q(category=category)
        else:
            cat_query = Q()
        if condition:
            con_quert = Q(condition=condition)
        else:
            con_quert = Q()
        ads = Ad.objects.filter(query, cat_query, con_quert, user=request.user.id)
        return render(request, "profile.html", {"username": request.user.username, "ads": ads})

def new_item_page(request):
    if request.user.is_authenticated:
        return render(request, "new_item.html")



def create_item(request):
    if request.method == "POST":
        name = request.POST.get("title")
        descript = request.POST.get("descript")
        url = request.POST.get("url")
        category = request.POST.get("category")
        condition = request.POST.get("condition")
        new_ad = Ad.objects.create(
            user=request.user.id,
            title=name,
            description=descript,
            image_url=url,
            category=category,
            condition=condition
        )
        new_ad.save()
        return redirect('/profile/')

def ad_page(request):
    ad_id = request.GET.get("id")
    ad = Ad.objects.filter(id=ad_id)[0]
    if ad.user == request.user.id:
        return render(request, "ad_page.html", {"ad": ad, })
    else:
        return HttpResponseForbidden()

def ad_edit(request):
    if request.method == "POST":
        id = request.POST.get("id")
        ad = Ad.objects.filter(id=id)[0]

        if ad.user == request.user.id:
            ad.title = request.POST.get("title")
            ad.description = request.POST.get("descript")
            ad.image_url = request.POST.get("url")
            ad.category = request.POST.get("category")
            ad.condition = request.POST.get("condition")
            ad.save()
            return redirect('/profile/')
        else:
            return render(request, "edit_error.html")

def logout_me(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/home/')

def market_page(request):
    search_text = request.GET.get('search', '')
    category = request.GET.get('category', '')
    condition = request.GET.get('condition', '')
    query = Q(title__icontains=search_text) | Q(description__icontains=search_text)
    if category:
        cat_query = Q(category=category)
    else:
        cat_query = Q()
    if condition:
        con_quert = Q(condition=condition)
    else:
        con_quert = Q()
    ads = Ad.objects.filter(query, cat_query, con_quert)
    return render(request, 'market.html', {"ads": ads, })

def new_trade_page(request):
    ad_id = request.GET.get("id")
    return render(request, 'new_trade.html', {"ad_id": ad_id, })

def create_trade(request):
    if request.user.is_authenticated:
        ad_id = request.POST.get("ad_id")
        ad_owner = Ad.objects.filter(id=ad_id)[0].user
        new_trade = ExchangeProposal.objects.create(
            ad_sender=request.user.id,
            ad_receiver=ad_owner,
            comment=request.POST.get("comment"),
        )
        new_trade.save()
        return redirect("/my_trades/")

def my_trades_page(request):
    if request.user.is_authenticated:
        search_text = request.GET.get('search', '')
        receiver = request.GET.get('receiver', '')
        status = request.GET.get('status', '')
        query = Q(comment__icontains=search_text)
        if receiver:
            cat_query = Q(ad_receiver=receiver)
        else:
            cat_query = Q()
        if status:
            con_quert = Q(status=status)
        else:
            con_quert = Q()
        my_trades = ExchangeProposal.objects.filter(query, cat_query, con_quert, ad_sender=request.user.id)
        return render(request, 'my_trades.html', {'trades': my_trades})


def trades_for_me_page(request):
    if request.user.is_authenticated:
        search_text = request.GET.get('search', '')
        sender = request.GET.get('sender', '')
        status = request.GET.get('status', '')
        query = Q(comment__icontains=search_text)
        if sender:
            cat_query = Q(ad_sender=sender)
        else:
            cat_query = Q()
        if status:
            con_quert = Q(status=status)
        else:
            con_quert = Q()
        my_trades = ExchangeProposal.objects.filter(query, cat_query, con_quert, ad_receiver=request.user.id)
        return render(request, 'new_trades.html', {'trades': my_trades})


def accept_trade(request):
    trade_id = request.GET.get("id")
    trade = ExchangeProposal.objects.filter(id=trade_id)[0]
    if trade.ad_receiver == request.user.id:
        trade.status = Status.ACCEPTED
        trade.save()
        return redirect('/new_trades/')

def deny_trade(request):
    trade_id = request.GET.get("id")
    trade = ExchangeProposal.objects.filter(id=trade_id)[0]
    if trade.ad_receiver == request.user.id:
        trade.status = Status.DENIED
        trade.save()
        return redirect('/new_trades/')

def delete_ad(request):
    ad = Ad.objects.filter(id=request.POST.get("id"))
    if len(ad) > 0:
        if ad[0].user == request.user.id:
            ad[0].delete()
            return redirect('/profile/')
    return render(request, "del_error.html")