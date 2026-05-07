from rest_framework import viewsets, permissions
from .models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer
from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing products.
    """
    queryset = Product.objects.select_related('category').all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        is_trending = self.request.query_params.get('is_trending', None)
        search = self.request.query_params.get('search', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        ordering = self.request.query_params.get('ordering', '-created_at')
        
        if category:
            queryset = queryset.filter(category_id=category)
        if is_trending is not None:
            queryset = queryset.filter(is_trending=is_trending.lower() == 'true')
        if search:
            queryset = queryset.filter(name__icontains=search)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        valid_orderings = ['price', '-price', 'name', '-name', 'created_at', '-created_at']
        if ordering in valid_orderings:
            queryset = queryset.order_by(ordering)
            
        return queryset

class CategoryListView(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing categories.
    """
    from django.db.models import Count
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
