import React from 'react';
import { Navigate } from 'react-router-dom';
import jwt_decode from 'jwt-decode'; // Default import

const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        return <Navigate to="/login" />;
    }

    try {
        const decoded = jwt_decode(token);
        const currentTime = Date.now() / 1000;
        if (decoded.exp < currentTime) {
            // Token has expired
            return <Navigate to="/login" />;
        }
    } catch (error) {
        console.error('Token decoding failed:', error);
        return <Navigate to="/login" />;
    }
    
    return children;
};

export default PrivateRoute;