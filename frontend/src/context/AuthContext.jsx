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
        await api.post('auth/login/', { username, password });

        try {
            // After successful login, fetch the profile to get user data
            // This also verifies if the session cookie was correctly set and sent
            const profileResponse = await api.get('auth/profile/');
            setUser(profileResponse.data);
            setLoading(false);
            return profileResponse.data;
        } catch (error) {
            console.error('Session establishment failed after login. This is likely a cookie/CORS issue.', error);
            // If profile fails after login, it's usually a SameSite/Secure cookie issue
            throw new Error('Session could not be established. Please check your browser cookie settings or CORS configuration.', { cause: error });
        }
    };

    const register = async (userData) => {
        await api.post('auth/register/', userData);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, register, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export { useAuth } from './useAuth';
