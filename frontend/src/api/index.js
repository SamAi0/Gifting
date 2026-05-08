import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
if (!API_BASE_URL) {
  console.warn('VITE_API_BASE_URL is not defined in environment variables.');
}

export const getImageUrl = (path) => {
  if (!path) return '';

  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }

  const baseUrl = API_BASE_URL.replace(/\/api\/?$/, '');
  const formattedPath = path.startsWith('/') ? path : `/${path}`;
  return encodeURI(`${baseUrl}${formattedPath}`);
};

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// Response interceptor to handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Don't warn for initial profile check as it's a normal part of auth flow
      if (!error.config.url.includes('auth/profile/') && !error.config.url.includes('auth/logout/')) {
        console.warn('Unauthorized request detected.');
      }
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
