from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("product/<int:product_id>", views.product_view, name="product"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("mylistings", views.my_listings, name="my_listings"),
    path("createlisting", views.create_listing, name="createlisting"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("<int:product_id>/placebid", views.place_bid, name="placebid"),
    path("<int:product_id>/add_to_watchlist", views.add_to_watch_list, name="add_watchlist"),
    path("<int:product_id>/closelisting", views.close_listing, name="close_listing"),
    path("<int:product_id>/add_comment", views.new_comment, name="new_comment")
]
