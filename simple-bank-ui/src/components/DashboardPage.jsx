import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import EmptyState from "./common/EmptyState";
import ErrorMessage from "./common/ErrorMessage";
import LoadingState from "./common/LoadingState";
import ThemeToggle from "./common/ThemeToggle";
import { clearSession, getSession } from "../services/apiClient";
import { getMyAccounts, getMyTransactions, getMyCashFlow, getAdminUsers, getAdminAccounts, getAdminTransactions } from "../services/accountApi";
import "./DashboardPage.css";

const money = value => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(Number(value || 0));

function DataTable({ title, rows, columns, empty, onRetry, loading, transferActions = false }) {
    return <section className="dashboard-panel"><div className="panel-heading"><h2>{title}</h2><button className="small-button" onClick={onRetry} disabled={loading}>Retry</button></div>{loading ? <LoadingState message="Loading…" className="muted" /> : !rows.length ? <EmptyState message={empty} className="empty-state" /> : <div className="table-wrap"><table><thead><tr>{columns.map(c => <th key={c.key}>{c.label}</th>)}{transferActions && <th>Action</th>}</tr></thead><tbody>{rows.map((r, i) => <tr key={r.userId || r.accountId || r.txnId || i}>{columns.map(c => <td key={c.key}>{String(r[c.key] ?? "—")}</td>)}{transferActions && <td><Link className="table-action" to={`/transfers?fromAccountId=${encodeURIComponent(r.accountId)}`}>Transfer</Link></td>}</tr>)}</tbody></table></div>}</section>;
}

export default function DashboardPage({ admin = false }) {
    const [data, setData] = useState({ users: [], accounts: [], transactions: [] });
    const [cashFlow, setCashFlow] = useState(null);
    const [loading, setLoading] = useState(false); const [error, setError] = useState("");
    const session = getSession(); const navigate = useNavigate();
    const load = useCallback(async () => {
        setLoading(true); setError("");
        try {
            if (admin) {
                const results = await Promise.all([getAdminUsers(), getAdminAccounts(), getAdminTransactions()]);
                setData({ users: results[0], accounts: results[1], transactions: results[2] });
            } else {
                const results = await Promise.all([getMyAccounts(), getMyTransactions(), getMyCashFlow(90)]);
                setData({ users: [], accounts: results[0], transactions: results[1] }); setCashFlow(results[2]);
            }
        } catch (e) { setError(e.message); }
        finally { setLoading(false); }
    }, [admin]);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    useEffect(() => { load(); }, [load]);
    function logout() { clearSession(); navigate("/login", { replace: true }); }
    return <main className="dashboard-page"><header className="dashboard-header"><Link to="/" className="dashboard-brand">Simple Bank</Link><nav><Link to={admin ? "/admin/dashboard" : "/dashboard"}>Dashboard</Link><Link to="/accounts">Accounts</Link><Link to="/transactions">Deposit / Withdraw</Link>{!admin && <><Link to="/analytics">Analytics</Link><Link to="/transfers">Transfers</Link></>}{admin && <><Link to="/users">User Management</Link><Link to="/admin/fraud-alerts">Fraud monitoring</Link></>}<ThemeToggle /><button onClick={logout} className="logout-button">Sign out</button></nav></header>
        <section className="dashboard-hero"><div><p className="dashboard-eyebrow">{admin ? "ADMINISTRATION" : "CUSTOMER PORTAL"}</p><h1>{admin ? "Admin dashboard" : `Welcome${session?.name ? `, ${session.name}` : " back"}`}</h1><p>{admin ? "Review users, accounts, transactions, and administrator-only risk alerts." : "Manage your accounts, track cash flow, and review your transaction history."}</p>{!admin && session?.userId && <p className="dashboard-user-id"><strong>Your User ID:</strong> <code>{session.userId}</code><span>Use this ID when opening an account.</span></p>}</div><div className="role-chip">{admin ? "AdminToken" : "CustomerToken"}</div></section>
        {error && <ErrorMessage message={error} onRetry={load} disabled={loading} retryLabel={loading ? "Retrying…" : "Retry"} className="dashboard-error" />}
        <div className="dashboard-actions"><Link to="/accounts">{admin ? "Create / find an account" : "Open a new account"}</Link><Link to="/transactions">Make a deposit or withdrawal</Link>{!admin && <><Link to="/transfers">Transfer between accounts</Link><Link to="/analytics">View cash-flow analytics</Link></>}{admin && <Link to="/admin/fraud-alerts">Review fraud / anomaly alerts</Link>}</div>
        {!admin && cashFlow && <section className="dashboard-cashflow"><div><span>Deposits · last 90 days</span><strong>{money(cashFlow.totals?.deposits)}</strong></div><div><span>Withdrawals · last 90 days</span><strong>{money(cashFlow.totals?.withdrawals)}</strong></div><div><span>Net external cash flow</span><strong>{money(cashFlow.netExternalCashFlow)}</strong></div><Link to="/analytics">View full analytics →</Link></section>}
        <div className="dashboard-grid">{admin && <DataTable title="All users" rows={data.users} columns={[{key:"userId",label:"User ID"},{key:"name",label:"Name"},{key:"email",label:"Email"}]} empty="No users found." onRetry={load} loading={loading} />}<DataTable title={admin ? "All accounts" : "My accounts"} rows={data.accounts} columns={[{key:"accountId",label:"Account ID"},{key:"userId",label:"Owner ID"},{key:"accountType",label:"Type"},{key:"balance",label:"Balance"}]} empty="No accounts yet. Create an account to get started." onRetry={load} loading={loading} transferActions={!admin && data.accounts.length > 1} /><DataTable title={admin ? "All transactions" : "My transactions"} rows={data.transactions} columns={[{key:"txnId",label:"Transaction ID"},{key:"accountId",label:"Account ID"},{key:"type",label:"Type"},{key:"amount",label:"Amount"},{key:"createdAt",label:"Date"}]} empty="No transactions recorded yet." onRetry={load} loading={loading} /></div>
    </main>;
}
