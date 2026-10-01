import { apiRequest, saveSession } from "./apiClient";

async function authenticate(path, payload) {
    const result = await apiRequest(path, {
        method: "POST",
        body: JSON.stringify(payload)
    });
    saveSession(result);
    return result;
}

export const registerCustomer = (payload) => authenticate("/auth/register", payload);
export const loginCustomer = (payload) => authenticate("/auth/login", payload);
export const setupAdmin = (payload) => authenticate("/auth/admin/setup", payload);
export const loginAdmin = (payload) => authenticate("/auth/admin/login", payload);
export const getCurrentUser = () => apiRequest("/auth/me");
