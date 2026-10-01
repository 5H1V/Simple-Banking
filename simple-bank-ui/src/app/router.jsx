import { BrowserRouter, Route, Routes } from "react-router-dom";
import AccountsPage from "../components/AccountsPage.jsx";
import App from "../App.jsx";
import AuthPage from "../components/AuthPage.jsx";
import DashboardPage from "../components/DashboardPage.jsx";
import NotFound from "../components/NotFound.jsx";
import ProtectedRoute from "../components/ProtectedRoute.jsx";
import TransactionsPage from "../components/TransactionsPage.jsx";
import WelcomePage from "../components/WelcomePage.jsx";
import TransferPage from "../components/TransferPage.jsx";
import AnalyticsPage from "../components/AnalyticsPage.jsx";
import FraudAlertsPage from "../components/FraudAlertsPage.jsx";

export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<WelcomePage />} />
                <Route path="/login" element={<AuthPage />} />
                <Route path="/register" element={<AuthPage mode="register" />} />
                <Route
                    path="/admin/setup"
                    element={<AuthPage mode="admin-setup" />}
                />

                <Route element={<ProtectedRoute />}>
                    <Route path="/accounts" element={<AccountsPage />} />
                    <Route path="/transactions" element={<TransactionsPage />} />
                </Route>

                <Route element={<ProtectedRoute roles={["CustomerToken"]} />}>
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/transfers" element={<TransferPage />} />
                    <Route path="/analytics" element={<AnalyticsPage />} />
                </Route>

                <Route element={<ProtectedRoute roles={["AdminToken"]} />}>
                    <Route path="/users" element={<App />} />
                    <Route
                        path="/admin/dashboard"
                        element={<DashboardPage admin />}
                    />
                    <Route path="/admin/fraud-alerts" element={<FraudAlertsPage />} />
                </Route>

                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
}