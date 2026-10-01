const API_BASE_URL = (
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api"
).replace(/\/+$/, "");
const SESSION_KEY = "simpleBankSession";

export function getSession() {
    try {
        const value = localStorage.getItem(SESSION_KEY);
        return value ? JSON.parse(value) : null;
    } catch (error) {
        localStorage.removeItem(SESSION_KEY);
        throw new Error("Saved sign-in data is invalid. Please sign in again.", {
            cause: error
        });
    }
}

export function getToken() {
    return getSession()?.accessToken || null;
}

export function getRole() {
    return getSession()?.role || null;
}

export function saveSession(session) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearSession() {
    localStorage.removeItem(SESSION_KEY);
}

export async function apiRequest(path, options = {}) {
    const headers = new Headers(options.headers || {});
    const token = getToken();
    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }
    if (options.body && !headers.has("Content-Type")) {
        headers.set("Content-Type", "application/json");
    }

    let response;
    try {
        response = await fetch(`${API_BASE_URL}${path}`, {
            ...options,
            headers
        });
    } catch (error) {
        if (error instanceof TypeError) {
            throw new Error(
                `Unable to reach the banking API at ${API_BASE_URL}. Check that the API is running and the address is correct.`,
                { cause: error }
            );
        }
        throw error;
    }

    if (response.status === 204) {
        return null;
    }
    const contentType = response.headers.get("content-type") || "";
    const body = contentType.includes("application/json")
        ? await response.json()
        : await response.text();
    if (!response.ok) {
        const detail = body && typeof body === "object" ? body.detail : null;
        throw new Error(
            typeof detail === "string"
                ? detail
                : `Request failed with status ${response.status}`
        );
    }
    return body;
}