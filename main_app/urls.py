from . import views
from django.urls import path

urlpatterns = [ 
	path('', views.home, name='home'),
	
	path('about/', views.about, name='about'),
	path('contactus/', views.contactus, name='contactus'),
	path('location/', views.location, name='location'),
	
	path('products/', views.products_index, name="index"),
	path('products/<int:product_id>/', views.products_detail, name="detail"),
	path('products/create/', views.ProductCreate.as_view(), name='products_create'),

	path('shoppingcarts/', views.shoppingcarts_index, name='shoppingcarts_index'),
	path('shoppingcarts/add/<int:product_id>/', views.shoppingcarts_add, name='shoppingcarts_add'),
	path('shoppingcarts/<int:id>/', views.shoppingcarts_delete, name="shoppingcarts_delete"),

	path('checkouts/', views.checkouts_index, name='checkouts_index'),

	path('account/signup', views.signup, name='signup'),

	path('search/', views.search_view, name='search'),
]