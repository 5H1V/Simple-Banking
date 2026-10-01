import { useState } from "react";
import { Link } from "react-router-dom";

import { submitTransaction } from "../services/accountApi";
import "./TransactionsPage.css";

function TransactionsPage() {
    const [accountId, setAccountId] = useState("");
    const [type, setType] = useState("deposit");
    const [amount, setAmount] = useState("");
    const [pending, setPending] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (pending) return;

        setError("");
        setResult(null);

        const id = accountId.trim();
        const value = Number(amount);
        if (!id) {
            setError("Enter an account ID.");
            return;
        }
        if (!/^\d+(?:\.\d{1,2})?$/.test(amount) || !Number.isFinite(value) || value <= 0) {
            setError("Enter a positive amount with at most two decimal places.");
            return;
        }

        setPending(true);
        try {
            const account = await submitTransaction(id, type, value);
            setResult({ type, account });
            setAmount("");
        } catch (requestError) {
            setError(requestError.message);
        } finally {
            setPending(false);
        }
    };

    return (
        <div className="transactions-page">
            <header className="transactions-header">
                <Link to="/" className="transactions-brand">Simple Bank</Link>
                <nav aria-label="Main navigation">
                    <Link to="/">Home</Link>
                    <Link to="/accounts">Accounts</Link>
                    <Link to="/users">User Management</Link>
                </nav>
            </header>

            <main className="transactions-main">
                <h1>Deposit or withdraw</h1>
                <p>Enter an existing account ID to make a transaction.</p>

                <form onSubmit={handleSubmit} className="transactions-form">
                    <label htmlFor="transaction-account">Account ID</label>
                    <input
                        id="transaction-account"
                        value={accountId}
                        onChange={(event) => setAccountId(event.target.value)}
                        required
                        disabled={pending}
                        autoComplete="off"
                    />

                    <label htmlFor="transaction-type">Transaction</label>
                    <select
                        id="transaction-type"
                        value={type}
                        onChange={(event) => setType(event.target.value)}
                        disabled={pending}
                    >
                        <option value="deposit">Deposit</option>
                        <option value="withdraw">Withdraw</option>
                    </select>

                    <label htmlFor="transaction-amount">Amount</label>
                    <input
                        id="transaction-amount"
                        type="number"
                        min="0.01"
                        step="0.01"
                        value={amount}
                        onChange={(event) => setAmount(event.target.value)}
                        required
                        disabled={pending}
                    />

                    <button type="submit" disabled={pending}>
                        {pending ? "Processing..." : type === "deposit" ? "Deposit" : "Withdraw"}
                    </button>
                </form>

                {error && <p className="transactions-error" role="alert">{error}</p>}
                {result && (
                    <div className="transactions-success" role="status">
                        <p>{result.type === "deposit" ? "Deposit" : "Withdrawal"} completed.</p>
                        <p>Account ID: {result.account.accountId}</p>
                        <p>Current balance: {result.account.balance}</p>
                    </div>
                )}
            </main>
        </div>
    );
}

export default TransactionsPage;
