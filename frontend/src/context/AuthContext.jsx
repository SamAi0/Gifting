import { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import api from '../api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState(() => {
        // Initialize from localStorage only - no side effects
        return localStorage.getItem('token');
    });

    // Validate token and set user after initialization
    useEffect(() => {
        let isMounted = true;
        
        const validateToken = async () => {
            if (!token) {
                if (isMounted) {
                    setUser(null);
                    setLoading(false);
                }
                return;
            }
            
            try {
                const decoded = jwtDecode(token);
                if (decoded.exp * 1000 < Date.now()) {
                    // Token expired
                    localStorage.removeItem('token');
                    if (isMounted) {
                        setToken(null);
                        setUser(null);
                    }
                } else {
                    if (isMounted) {
                        setUser(decoded);
                    }
                }
            } catch {
                // Invalid token
                localStorage.removeItem('token');
                if (isMounted) {
                    setToken(null);
                    setUser(null);
                }
            }
            if (isMounted) {
                setLoading(false);
            }
        };
        
        validateToken();
        
        return () => {
            isMounted = false;
        };
    }, [token]);

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        setLoading(false);
    };

    const login = async (username, password) => {
        const response = await api.post('/auth/login/', { username, password });
        const { access } = response.data;
        localStorage.setItem('token', access);
        setToken(access);
        const decoded = jwtDecode(access);
        setUser(decoded);
        setLoading(false);
        return response.data;
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export { useAuth } from './useAuth';
