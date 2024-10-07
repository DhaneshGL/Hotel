import { Navigate, Outlet } from 'react-router-dom';
import AuthService from './services/AuthService';

const PrivateRoute = () => {
  const isAuthenticated = AuthService.getCurrentUser() !== null && AuthService.getCurrentUser() !== undefined;

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
