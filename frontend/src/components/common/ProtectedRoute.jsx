import React from 'react';
import { Navigate } from 'react-router-dom';
import authService from '../../services/auth.service';

const ProtectedRoute = ({ children, requiredRole }) => {
    const user = authService.getCurrentUser();
    const isAuthenticated = authService.isAuthenticated();

    if (!isAuthenticated) {
        return <Navigate to="/" replace />;
    }

    if (requiredRole && user?.role !== requiredRole) {
        return <Navigate to="/" replace />;
    }

    return children;
};

export default ProtectedRoute;
