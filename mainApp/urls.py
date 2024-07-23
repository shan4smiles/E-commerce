from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('login/', views.authenticate_user, name = 'authenticate_user'),
    path('login_again/', views.logout_user, name = 'logout'),

    path('', views.home, name = 'home'),
    path('index/', views.index, name = 'index'),
    path('register/', views.register_user, name = 'register_user'),
    path('add_product/', views.add_product, name = 'add_product'),

    path('product_list/', views.product_list, name = 'product_list'),
    path('product_details/<int:pk>/', views.product_details, name = 'product_detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)