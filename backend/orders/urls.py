from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CartView, CartItemViewSet, AddressViewSet, 
    CreateOrderView, VerifyPaymentView, OrderViewSet,
    UserOrderListView, PincodeCheckView, MergeCartView, ValidateCouponView,
    SaveForLaterViewSet
)

router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet, basename='cart-item')
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'all-orders', OrderViewSet, basename='all-orders')
router.register(r'save-for-later', SaveForLaterViewSet, basename='save-for-later')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('mine/', UserOrderListView.as_view(), name='user-orders'),
    path('check-pincode/', PincodeCheckView.as_view(), name='check-pincode'),
    path('merge-cart/', MergeCartView.as_view(), name='merge-cart'),
    path('coupons/validate/', ValidateCouponView.as_view(), name='validate-coupon'),
]
