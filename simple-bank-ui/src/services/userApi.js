import { apiRequest } from "./apiClient";

export async function getAllUsers() {
    return apiRequest("/users");
}

export async function getUserById(userId) {
    return apiRequest(`/users/${encodeURIComponent(userId)}`);
}

export async function createUser(user) {
    return apiRequest("/users", {
        method: "POST",
        body: JSON.stringify(user)
    });
}

export async function updateUser(userId, user) {
    return apiRequest(`/users/${encodeURIComponent(userId)}`, {
        method: "PUT",
        body: JSON.stringify(user)
    });
}

export async function deleteUser(userId) {
    return apiRequest(`/users/${encodeURIComponent(userId)}`, {
        method: "DELETE"
    });
}