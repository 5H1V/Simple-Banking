const API_URL = "http://127.0.0.1:5000/api/accounts";

async function readResponse(response, fallbackMessage) {
    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            typeof error.detail === "string"
                ? error.detail
                : fallbackMessage
        );
    }

    return response.json();
}

export async function createAccount(userId, accountType) {
    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ userId, accountType })
    });

    return readResponse(response, "Failed to create account");
}

export async function getAccountById(accountId) {
    const response = await fetch(
        `${API_URL}/${encodeURIComponent(accountId)}`
    );

    return readResponse(response, "Account not found");
}

export async function submitTransaction(accountId, type, amount) {
    const response = await fetch(
        `${API_URL}/${encodeURIComponent(accountId)}/${type}`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ amount })
        }
    );

    return readResponse(response, "Transaction failed");
}
