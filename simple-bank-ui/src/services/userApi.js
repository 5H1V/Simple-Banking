const API_URL = "http://127.0.0.1:5000/api/users";

export async function getAllUsers() {
    const response = await fetch(API_URL);
    if (!response.ok) {
        throw new Error("Failed to get users");
    }
    return response.json();
}

export async function getUserById(userId) {
    const response = await fetch(
        `${API_URL}/${userId}`
    );
    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.detail || "User not found"
        );
    }

    return response.json();
}

export async function createUser(user) {
    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(user)
    });
    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.detail || "Failed to create user"
        );
    }

    return response.json();
}

export async function updateUser(userId, user) {
    const response = await fetch(
        `${API_URL}/${userId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(user)
        }
    );
    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.detail || "Failed to update user"
        );
    }

    return response.json();
}

export async function deleteUser(userId) {
    const response = await fetch(
        `${API_URL}/${userId}`,
        {
            method: "DELETE"
        }
    );
    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.detail || "Failed to delete user"
        );
    }

    return response.json();
}