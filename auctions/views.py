from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import decimal
from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "products": Product.objects.order_by("-date_posted").all()
    })


def product_view(request, product_id):

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        watch_list = user.watchlist.all()
    else:
        watch_list = []

    product = Product.objects.get(id=product_id)

    comments = Comment.objects.filter(product=product)

    if product not in watch_list:
        button_text = "Add to watchlist"
        button_class = "btn btn-primary"
    else:
        button_text = "Remove from watchlist"
        button_class = "btn btn-danger"

    return render(request, "auctions/product.html", {
        "product": product,
        "button": button_text,
        "button_class": button_class,
        "comments": comments,
    })


def categories(request):
    categories_all = Category.objects.order_by("category").all()
    return render(request, "auctions/categories.html", {
        "categories": categories_all
    })


def category(request, category_id):
    cat = Category.objects.get(id=category_id)
    products = cat.products.filter(active=True).all()
    products_off = cat.products.filter(active=False).all()
    return render(request, "auctions/category.html", {
        "products": products,
        "products_off": products_off,
        "category": cat
    })


def watchlist(request):
    user = User.objects.get(username=request.user.username)
    watch_list = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist": watch_list
    })


def my_listings(request):
    user = User.objects.get(username=request.user.username)
    products = user.listings.all()

    return render(request, "auctions/my_listings.html", {
        "my_listings": products
    })


def new_comment(request, product_id):

    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        try:
            comment_text = request.POST["new_comment"]
            comment = Comment(user=request.user, product=product, comment=comment_text)
            comment.save()
            return HttpResponseRedirect(reverse("product", args=(product.id,)))
        except:
            return HttpResponseRedirect(reverse("product", args=(product.id,)))
    else:
        return HttpResponseRedirect(reverse("product", args=(product.id,)))


def add_to_watch_list(request, product_id):
    user = User.objects.get(username=request.user.username)
    product = Product.objects.get(id=product_id)
    watch_list = user.watchlist.all()

    if product in watch_list:
        user.watchlist.remove(product)
    else:
        user.watchlist.add(product)

    return HttpResponseRedirect(reverse('product', args=(product.id, )))


def close_listing(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.user.username == product.seller.username:
        product.active = False
        product.save()

    return HttpResponseRedirect(reverse('product', args=(product.id,)))


def create_listing(request):
    if request.method == "GET":
        categories_listing = Category.objects.all()

        return render(request, "auctions/createlisting.html", {
            "categories": categories_listing
        })
    else:
        seller = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        initial_bid = request.POST["initial_bid"]
        image_url = request.POST["image_url"]
        cat_name = request.POST['categoria']
        cat = Category.objects.get(category=cat_name)
        listing = Product(seller=seller,
                          title=title,
                          description=description,
                          initial_bid=initial_bid,
                          current_bid=initial_bid,
                          image_url=image_url,
                          category=cat
                          )

        listing.save()
        return HttpResponseRedirect(reverse("createlisting"))


def place_bid(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            bid = float(request.POST["bid"])

            if bid > product.current_bid:
                new_bid = Bid(bidder=request.user, product=product, bid=bid)

                product.buyer = request.user
                product.current_bid = bid

                new_bid.save()
                product.save()
                return HttpResponseRedirect(reverse("product", args=(product.id,)))
            else:
                return HttpResponseRedirect(reverse("product", args=(product.id,)))
        except:
            return HttpResponseRedirect(reverse("product", args=(product.id,)))
    else:
        return HttpResponseRedirect(reverse("product", args=(product_id,)))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
