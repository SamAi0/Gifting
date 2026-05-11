from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Product, Category, Review, Wishlist, Attribute
from api.serializers import (
    ProductSerializer, CategorySerializer, ReviewSerializer, 
    WishlistSerializer, AttributeValueSerializer
)
from api.permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeValueSerializer # We use this to show attributes and their values if needed
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

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
                queryset = queryset.filter(stock__gt=0, is_active=True)
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

    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response([])
        
        products = Product.objects.filter(name__icontains=query)[:5]
        categories = Category.objects.filter(name__icontains=query)[:3]
        
        results = []
        for p in products:
            results.append({"type": "product", "id": p.id, "text": p.name, "slug": p.slug})
        for c in categories:
            results.append({"type": "category", "id": c.id, "text": c.name})
            
        return Response(results)

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        product = self.get_object()
        related = Product.objects.filter(category=product.category).exclude(id=product.id).order_by('-popularity_score')[:4]
        serializer = self.get_serializer(related, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def frequently_bought_together(self, request, pk=None):
        from orders.models import OrderItem
        product = self.get_object()
        # Find orders that contains this product
        order_ids = OrderItem.objects.filter(product=product).values_list('order_id', flat=True)
        # Find other products in those orders
        other_products = OrderItem.objects.filter(order_id__in=order_ids).exclude(product=product).values('product').annotate(count=Count('product')).order_by('-count')[:4]
        
        product_ids = [item['product'] for item in other_products]
        recommended = Product.objects.filter(id__in=product_ids)
        serializer = self.get_serializer(recommended, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def recently_viewed(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response([])
        # Maintain order of IDs provided
        from django.db.models import Case, When
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        products = Product.objects.filter(id__in=ids).order_by(preserved)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

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

    def get_queryset(self):
        queryset = Review.objects.all()
        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        product = serializer.validated_data.get('product')
        user = self.request.user
        
        if Review.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError({"detail": "You have already reviewed this product."})
            
        serializer.save(user=user)

    def perform_update(self, serializer):
        instance = self.get_object()
        # Check if the review is older than 4 minutes
        if timezone.now() > instance.created_at + timedelta(minutes=4):
            raise serializers.ValidationError({"detail": "Editing window (4 minutes) has expired. You can no longer edit this review."})
        serializer.save()

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

