from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Count
from .models import Product, Category, Review, Wishlist
from api.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, WishlistSerializer
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
        queryset = Product.objects.select_related('category').all()
        category = self.request.query_params.get('category', None)
        is_trending = self.request.query_params.get('is_trending', None)
        is_available = self.request.query_params.get('is_available', None)
        on_sale = self.request.query_params.get('on_sale', None)
        min_rating = self.request.query_params.get('min_rating', None)
        search = self.request.query_params.get('search', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        ordering = self.request.query_params.get('ordering', '-created_at')
        
        if category:
            queryset = queryset.filter(category_id=category)
        if is_trending is not None:
            queryset = queryset.filter(is_trending=is_trending.lower() == 'true')
        if is_available is not None:
            if is_available.lower() == 'true':
                queryset = queryset.filter(stock__gt=0)
        if on_sale is not None:
            if on_sale.lower() == 'true':
                queryset = queryset.filter(discount_price__isnull=False)
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
            
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(sku__icontains=search) |
                Q(tags__icontains=search) |
                Q(category__name__icontains=search)
            ).distinct()

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        valid_orderings = ['price', '-price', 'name', '-name', 'created_at', '-created_at', 'popularity_score', '-popularity_score', 'average_rating', '-average_rating']
        if ordering in valid_orderings:
            queryset = queryset.order_by(ordering)
            
        return queryset

class CategoryListView(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing categories.
    """
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # Ensure user can only review if they purchased (logic to be added)
        serializer.save(user=self.request.user)

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

