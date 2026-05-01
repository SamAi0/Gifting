import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://gifting-5pic.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add a request interceptor to attach the JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth endpoints
export const loginUser = (credentials) => api.post('/auth/login/', credentials);
export const registerUser = (userData) => api.post('/auth/register/', userData);

// Product endpoints
export const fetchProducts = (params) => api.get('/products/', { params });
export const fetchProductById = (id) => api.get(`/products/${id}/`);
export const fetchCategories = () => api.get('/categories/');
export const createProduct = (formData) => api.post('/products/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
export const updateProduct = (id, formData) => api.patch(`/products/${id}/`, formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
export const deleteProduct = (id) => api.delete(`/products/${id}/`);

// Order & Cart endpoints
export const fetchCart = () => api.get('/orders/cart/');
export const addToCart = (data) => api.post('/orders/cart-items/', data);
export const updateCartItem = (id, data) => api.patch(`/orders/cart-items/${id}/`, data);
export const removeCartItem = (id) => api.delete(`/orders/cart-items/${id}/`);
export const fetchAddresses = () => api.get('/orders/addresses/');
export const addAddress = (data) => api.post('/orders/addresses/', data);
export const createOrder = (data) => api.post('/orders/create-order/', data);

// Inquiry & Other endpoints
export const fetchTestimonials = () => api.get('/testimonials/');
export const fetchSettings = () => api.get('/settings/');
export const submitContact = (data) => api.post('/contact/', data);
export const submitBulkInquiry = (formData) => api.post('/bulk-inquiry/', formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export default api;
