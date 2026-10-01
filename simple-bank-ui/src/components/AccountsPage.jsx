import { useState } from "react";
import { Link } from "react-router-dom";

import { createAccount, getAccountById } from "../services/accountApi";
import { getRole, getSession } from "../services/apiClient";
import ThemeToggle from "./common/ThemeToggle";
import "./AccountsPage.css";

function AccountDetails({ account }) {
    return (
        <section className="account-result" aria-live="polite">
            <h2>Account details</h2>
            <dl>
                <div>
                    <dt>Account ID</dt>
                    <dd>{account.accountId}</dd>
                </div>
                <div>
                    <dt>User ID</dt>
                    <dd>{account.userId}</dd>
                </div>
                <div>
                    <dt>Account type</dt>
                    <dd>{account.accountType}</dd>
                </div>
                <div>
                    <dt>Balance</dt>
                    <dd>{Number(account.balance).toFixed(2)}</dd>
                </div>
            </dl>
        </section>
    );
}

function AccountsPage() {
    const session = getSession();
    const isCustomer = getRole() === "CustomerToken";
    const [userId, setUserId] = useState(session?.userId ?? "");
    const [accountType, setAccountType] = useState("Checking");
    const [searchId, setSearchId] = useState("");
    const [createdAccount, setCreatedAccount] = useState(null);
    const [searchedAccount, setSearchedAccount] = useState(null);
    const [createError, setCreateError] = useState("");
    const [searchError, setSearchError] = useState("");
    const [creating, setCreating] = useState(false);
    const [searching, setSearching] = useState(false);

    const handleCreate = async (event) => {
        event.preventDefault();
        if (creating) return;

        setCreateError("");
        setCreatedAccount(null);
        setCreating(true);

        try {
            const account = await createAccount(userId.trim(), accountType);
            setCreatedAccount(account);
        } catch (error) {
            setCreateError(error.message);
        } finally {
            setCreating(false);
        }
    };

    const handleLookup = async (event) => {
        event.preventDefault();
        if (searching) return;

        const id = searchId.trim();
        if (!id) {
            setSearchError("Enter an account ID.");
            setSearchedAccount(null);
            return;
        }

        setSearchError("");
        setSearchedAccount(null);
        setSearching(true);
        try {
            setSearchedAccount(await getAccountById(id));
        } catch (error) {
            setSearchError(error.message);
        } finally {
            setSearching(false);
        }
    };

    return (
        <div className="accounts-page">
            <header className="accounts-header">
                <Link to="/" className="accounts-brand">Simple Bank</Link>
                <nav aria-label="Main navigation">
                    <Link to="/">Home</Link>
                    <Link to="/users">User Management</Link>
                    <Link to="/transactions">Deposit / Withdraw</Link>
                    <Link to="/dashboard">Dashboard</Link>
                    <ThemeToggle />
                </nav>
            </header>

            <main className="accounts-main">
                <h1>Accounts</h1>
                <p className="accounts-intro">{isCustomer ? "Create an account for yourself or look up an existing account." : "Create an account for a user or look up an existing account."}</p>

                <div className="accounts-grid">
                    <section className="account-panel">
                        <h2>Create an account</h2>
                        <form onSubmit={handleCreate} className="account-form">
                            <label htmlFor="account-user-id">User ID</label>
                            <input
                                id="account-user-id"
                                value={userId}
                                onChange={(event) => setUserId(event.target.value)}
                                required
                                readOnly={isCustomer}
                                disabled={creating}
                                autoComplete="off"
                            />
                            {isCustomer && <p className="accounts-intro">This is your User ID from your dashboard.</p>}

                            <label htmlFor="account-type">Account type</label>
                            <select
                                id="account-type"
                                value={accountType}
                                onChange={(event) => setAccountType(event.target.value)}
                                disabled={creating}
                            >
                                <option value="Checking">Checking</option>
                                <option value="Savings">Savings</option>
                            </select>

                            <button type="submit" disabled={creating}>
                                {creating ? "Creating..." : "Create account"}
                            </button>
                        </form>
                        {createError && <p className="account-error" role="alert">{createError}</p>}
                        {createdAccount && (
                            <>
                                <p className="account-success" role="status">Account created successfully.</p>
                                <AccountDetails account={createdAccount} />
                            </>
                        )}
                    </section>

                    <section className="account-panel">
                        <h2>View account details</h2>
                        <form onSubmit={handleLookup} className="account-form">
                            <label htmlFor="account-search-id">Account ID</label>
                            <input
                                id="account-search-id"
                                value={searchId}
                                onChange={(event) => setSearchId(event.target.value)}
                                required
                                disabled={searching}
                                autoComplete="off"
                            />
                            <button type="submit" disabled={searching}>
                                {searching ? "Looking up..." : "Find account"}
                            </button>
                        </form>
                        {searchError && <p className="account-error" role="alert">{searchError}</p>}
                        {searchedAccount && <AccountDetails account={searchedAccount} />}
                    </section>
                </div>
            </main>
        </div>
    );
}

export default AccountsPage;
