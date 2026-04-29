from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartView, CartItemViewSet, AddressViewSet, CreateOrderView, VerifyPaymentView

router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet, basename='cart-item')
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
]
