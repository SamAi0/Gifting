from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryListView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryListView)

urlpatterns = [
    path('', include(router.urls)),
]
