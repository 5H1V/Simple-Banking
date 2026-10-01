import os

os.environ.setdefault("MONGO_URI", "mongodb://127.0.0.1:27017")
os.environ.setdefault("JWT_SECRET_KEY", "test-only-secret-that-is-over-32-characters")
os.environ.setdefault("ADMIN_SETUP_KEY", "test-only-admin-key")

from app import app


def test_api_routes_are_registered_under_api_prefix():
    routes = {
        (route.path, method)
        for route in app.routes
        for method in getattr(route, "methods", set())
    }

    expected_routes = {
        ("/api/users", "GET"),
        ("/api/users", "POST"),
        ("/api/accounts", "POST"),
        ("/api/accounts/me", "GET"),
        ("/api/transactions/me", "GET"),
        ("/api/auth/register", "POST"),
        ("/api/auth/login", "POST"),
        ("/api/auth/admin/setup", "POST"),
        ("/api/admin/users", "GET"),
        ("/api/admin/accounts", "GET"),
        ("/api/admin/transactions", "GET"),
        ("/api/accounts/transfer", "POST"),
        ("/api/analytics/me/cash-flow", "GET"),
        ("/api/admin/fraud-alerts", "GET"),
        ("/api/admin/fraud-alerts/{alert_id}/review", "PATCH")
    }

    assert expected_routes <= routes