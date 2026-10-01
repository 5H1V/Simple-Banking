import { Navigate, Outlet, useLocation } from "react-router-dom";
import { getRole, getToken } from "../services/apiClient";

export default function ProtectedRoute({ roles }) {
    const location = useLocation();
    if (!getToken()) return <Navigate to="/login" replace state={{ from: location }} />;
    if (roles && !roles.includes(getRole())) {
        return <Navigate to={getRole() === "AdminToken" ? "/admin/dashboard" : "/dashboard"} replace />;
    }
    return <Outlet />;
}
