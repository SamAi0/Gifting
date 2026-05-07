import { createContext, useState, useEffect } from 'react';
import api from '../api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Fetch user profile on mount to check if already logged in via cookie
    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await api.get('auth/profile/');
                setUser(response.data);
            } catch {
                console.log('No active session');
                setUser(null);
            } finally {
                setLoading(false);
            }
        };
        
        checkAuth();
    }, []);

    const logout = async () => {
        try {
            await api.post('auth/logout/');
        } catch (error) {
            console.error('Logout error', error);
        } finally {
            setUser(null);
            setLoading(false);
        }
    };

    const login = async (username, password) => {
        const response = await api.post('auth/login/', { username, password });
        // Token is now set in HttpOnly cookie by backend
        // Fetch profile to get user info
        const profileResponse = await api.get('auth/profile/');
        setUser(profileResponse.data);
        setLoading(false);
        return response.data;
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export { useAuth } from './useAuth';
