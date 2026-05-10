import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
if (!API_BASE_URL) {
  console.warn('VITE_API_BASE_URL is not defined in environment variables.');
}

export const getImageUrl = (path, useCors = false) => {
  if (!path) return '';

  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }

  let formattedPath = path.startsWith('/') ? path : `/${path}`;
  
  // If useCors is true, we route through our custom CORS-enabled endpoints
  if (useCors) {
    if (formattedPath.startsWith('/static/')) {
      formattedPath = formattedPath.replace('/static/', '/cors-static/');
    } else if (formattedPath.startsWith('/media/')) {
      formattedPath = formattedPath.replace('/media/', '/cors-media/');
    }
  }

  const baseUrl = API_BASE_URL.replace(/\/api\/?$/, '');
  return encodeURI(`${baseUrl}${formattedPath}`);
};


const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// Response interceptor to handle global errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const status = error.response.status;
      const url = error.config.url;
      
      if (status === 401) {
        // Don't warn for initial profile check as it's a normal part of auth flow
        if (!url.includes('auth/profile/') && !url.includes('auth/logout/')) {
          console.warn('Unauthorized request detected. Redirecting to login or clearing session.');
        }
      } else if (status === 403) {
        console.error('Forbidden: You do not have permission to perform this action.');
      } else if (status === 429) {
        console.error('Too many requests: Please slow down.');
      } else if (status >= 500) {
        console.error('Server error: Our team has been notified. Please try again later.');
      }
    } else if (error.request) {
      console.error('Network error: Please check your internet connection.');
    } else {
      console.error('Request error:', error.message);
    }
    return Promise.reject(error);
  }
);


// Auth endpoints
export const loginUser = (credentials) => api.post('auth/login/', credentials);
export const logoutUser = () => api.post('auth/logout/');
export const registerUser = (userData) => api.post('auth/register/', userData);
export const fetchProfile = () => api.get('auth/profile/');

// Product endpoints
export const fetchProducts = (params) => api.get('products/', { params });
export const fetchProductById = (id) => api.get(`products/${id}/`);
export const fetchCategories = () => api.get('categories/');
export const createProduct = (formData) => api.post('products/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
export const updateProduct = (id, formData) => api.patch(`products/${id}/`, formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
export const deleteProduct = (id) => api.delete(`products/${id}/`);

// Review & Wishlist endpoints
export const fetchReviews = (params) => api.get('reviews/', { params });
export const submitReview = (data) => api.post('reviews/', data, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
export const fetchWishlist = () => api.get('wishlist/');
export const addToWishlist = (productId) => api.post('wishlist/', { product: productId });
export const removeFromWishlist = (id) => api.delete(`wishlist/${id}/`);
export const mergeCart = (items) => api.post('orders/merge-cart/', { items });


// Order & Cart endpoints
export const fetchCart = () => api.get('orders/cart/');
export const addToCart = (data) => api.post('orders/cart-items/', data);
export const updateCartItem = (id, data) => api.patch(`orders/cart-items/${id}/`, data);
export const removeCartItem = (id) => api.delete(`orders/cart-items/${id}/`);
export const fetchAddresses = () => api.get('orders/addresses/');
export const addAddress = (data) => api.post('orders/addresses/', data);
export const createOrder = (data) => api.post('orders/create-order/', data);

// Inquiry & Other endpoints
export const fetchTestimonials = () => api.get('testimonials/');
export const fetchSettings = () => api.get('settings/');
export const submitContact = (data) => api.post('contact/', data);

export default api;
