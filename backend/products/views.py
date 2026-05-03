from rest_framework import viewsets, permissions
from .models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing products.
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        is_trending = self.request.query_params.get('is_trending', None)
        search = self.request.query_params.get('search', None)
        ordering = self.request.query_params.get('ordering', '-created_at')
        
        if category:
            queryset = queryset.filter(category_id=category)
        if is_trending is not None:
            queryset = queryset.filter(is_trending=is_trending.lower() == 'true')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        valid_orderings = ['price', '-price', 'name', '-name', 'created_at', '-created_at']
        if ordering in valid_orderings:
            queryset = queryset.order_by(ordering)
            
        return queryset

class CategoryListView(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
