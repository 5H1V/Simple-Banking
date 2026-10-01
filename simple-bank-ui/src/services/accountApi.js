import { apiRequest } from "./apiClient";

export function createAccount(userId, accountType) {
    return apiRequest("/accounts", {
        method: "POST",
        body: JSON.stringify({ userId, accountType })
    });
}

export function getAccountById(accountId) {
    return apiRequest(`/accounts/${encodeURIComponent(accountId)}`);
}

export function submitTransaction(accountId, type, amount) {
    return apiRequest(
        `/accounts/${encodeURIComponent(accountId)}/${type}`,
        {
            method: "POST",
            body: JSON.stringify({ amount })
        }
    );
}

export function getMyAccounts() {
    return apiRequest("/accounts/me");
}

export function getMyTransactions() {
    return apiRequest("/transactions/me");
}

export function getAdminUsers() {
    return apiRequest("/admin/users");
}

export function getAdminAccounts() {
    return apiRequest("/admin/accounts");
}

export function getAdminTransactions() {
    return apiRequest("/admin/transactions");
}
