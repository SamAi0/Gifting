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
        try {
            await api.post('auth/login/', { username, password });

            // After successful login, fetch the profile to get user data
            // This also verifies if the session cookie was correctly set and sent
            const profileResponse = await api.get('auth/profile/');
            setUser(profileResponse.data);
            setLoading(false);
            return profileResponse.data;
        } catch (error) {
            console.error('Login or session establishment failed:', error);
            
            // Extract the specific error message from the backend if possible
            let errorMessage = 'The credentials you entered do not match our records.';
            
            if (error.response && error.response.data) {
                if (error.response.data.detail) {
                    errorMessage = error.response.data.detail;
                } else if (error.response.data.message) {
                    errorMessage = error.response.data.message;
                }
            } else if (error.message === 'Network Error') {
                errorMessage = 'Connection lost. Please check if the backend server is running.';
            }

            setUser(null);
            setLoading(false);
            throw new Error(errorMessage, { cause: error });
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
