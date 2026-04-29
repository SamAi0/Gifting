from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing products.
    Supports filtering by category, trending status, and search.
    """
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        is_trending = self.request.query_params.get('is_trending', None)
        search = self.request.query_params.get('search', None)
        ordering = self.request.query_params.get('ordering', '-created_at')
        
        if category:
            queryset = queryset.filter(category_id=category)
        if is_trending:
            queryset = queryset.filter(is_trending=True)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Apply ordering
        valid_orderings = ['price', '-price', 'name', '-name', 'created_at', '-created_at']
        if ordering in valid_orderings:
            queryset = queryset.order_by(ordering)
            
        return queryset


class CategoryListView(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
