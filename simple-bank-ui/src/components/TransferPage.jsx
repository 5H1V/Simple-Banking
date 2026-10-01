import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { getMyAccounts, transferBetweenAccounts } from "../services/accountApi";
import ThemeToggle from "./common/ThemeToggle";
import LoadingState from "./common/LoadingState";
import "./FeaturePages.css";

const money = value => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(Number(value || 0));
const label = account => `${account.accountType || "Account"} · ${String(account.accountId).slice(-6)} · ${money(account.balance)}`;

export default function TransferPage() {
    const [params] = useSearchParams();
    const requestedSource = params.get("fromAccountId") || "";
    const [accounts, setAccounts] = useState([]);
    const [fromId, setFromId] = useState(requestedSource);
    const [toId, setToId] = useState("");
    const [amount, setAmount] = useState("");
    const [loading, setLoading] = useState(true);
    const [pending, setPending] = useState(false);
    const [error, setError] = useState("");
    const [result, setResult] = useState(null);
    const [confirming, setConfirming] = useState(false);

    async function loadAccounts() {
        setError("");
        try {
            const rows = await getMyAccounts();
            setAccounts(rows);
            setFromId(current => rows.some(a => a.accountId === current) ? current : (rows[0]?.accountId || ""));
            setToId(current => rows.some(a => a.accountId === current && current !== fromId) ? current : (rows.find(a => a.accountId !== (rows.some(x => x.accountId === requestedSource) ? requestedSource : rows[0]?.accountId))?.accountId || ""));
        } catch (e) { setError(e.message); }
        finally { setLoading(false); }
    }
    // eslint-disable-next-line react-hooks/set-state-in-effect, react-hooks/exhaustive-deps
    useEffect(() => { loadAccounts(); }, []);

    const source = accounts.find(a => a.accountId === fromId);
    const destinationOptions = useMemo(() => accounts.filter(a => a.accountId !== fromId), [accounts, fromId]);
    const destination = accounts.find(a => a.accountId === toId);

    function changeSource(value) {
        setFromId(value);
        if (value === toId) setToId(accounts.find(a => a.accountId !== value)?.accountId || "");
        setResult(null); setConfirming(false);
    }

    async function submit(event) {
        event.preventDefault(); setError(""); setResult(null);
        if (!fromId || !toId || fromId === toId) { setError("Choose two different accounts."); return; }
        if (!/^\d+(?:\.\d{1,2})?$/.test(amount) || !Number.isFinite(Number(amount)) || Number(amount) <= 0) { setError("Enter a positive amount with at most two decimal places."); return; }
        if (Number(amount) > Number(source?.balance || 0)) { setError("The source account does not have enough funds."); return; }
        if (!confirming) { setConfirming(true); return; }
        setPending(true);
        try {
            const transfer = await transferBetweenAccounts(fromId, toId, Number(amount));
            setResult(transfer); setAmount(""); setConfirming(false); await loadAccounts();
        } catch (e) { setError(e.message); setConfirming(false); }
        finally { setPending(false); }
    }

    return <main className="feature-page"><header className="feature-header"><Link className="feature-brand" to="/dashboard">Simple Bank</Link><nav><Link to="/dashboard">Dashboard</Link><Link to="/accounts">Accounts</Link><Link to="/analytics">Analytics</Link><Link to="/transactions">Deposit / Withdraw</Link><ThemeToggle /></nav></header>
        <section className="feature-main"><p className="eyebrow">MOVE MONEY</p><h1>Transfer between accounts</h1><p className="feature-intro">Move funds between accounts you own. Transfers are shown separately from external deposits and withdrawals.</p>
            {loading ? <LoadingState message="Loading your accounts…" /> : accounts.length < 2 ? <section className="feature-card"><h2>You need at least two accounts</h2><p>Create another account before making an internal transfer.</p><Link className="primary-link" to="/accounts">Open an account</Link></section> : <form className="feature-card feature-form" onSubmit={submit}>
                <label htmlFor="transfer-from">Transfer from</label><select id="transfer-from" value={fromId} onChange={e => changeSource(e.target.value)} disabled={pending}>{accounts.map(a => <option key={a.accountId} value={a.accountId}>{label(a)}</option>)}</select>
                <p className="field-hint">Available balance: {money(source?.balance)}</p>
                <label htmlFor="transfer-to">Transfer to</label><select id="transfer-to" value={toId} onChange={e => { setToId(e.target.value); setResult(null); setConfirming(false); }} disabled={pending}>{destinationOptions.map(a => <option key={a.accountId} value={a.accountId}>{label(a)}</option>)}</select>
                <label htmlFor="transfer-amount">Amount (USD)</label><input id="transfer-amount" type="number" min="0.01" step="0.01" value={amount} onChange={e => { setAmount(e.target.value); setConfirming(false); }} required disabled={pending} />
                {destination && <div className="transfer-review"><strong>Transfer summary</strong><span>{label(source || {})}</span><span aria-hidden="true">↓</span><span>{label(destination)}</span><span>Amount: {money(amount || 0)}</span></div>}
                {confirming && <div className="confirmation-panel" role="status"><strong>Confirm this transfer</strong><p>Transfer {money(amount)} from {source?.accountType} ending {String(fromId).slice(-6)} to {destination?.accountType} ending {String(toId).slice(-6)}?</p><p>This action updates both account balances and creates transaction history entries.</p></div>}
                <div className="transfer-actions"><button type="submit" disabled={pending}>{pending ? "Processing transfer…" : confirming ? "Confirm transfer" : "Review transfer"}{!confirming && " →"}</button>{confirming && <button type="button" className="button-secondary" onClick={() => setConfirming(false)} disabled={pending}>Cancel</button>}</div>
            </form>}
            {error && <p className="feature-error" role="alert">{error}</p>}
            {result && <section className="feature-success" role="status"><h2>Transfer completed</h2><p>{money(result.amount)} was transferred successfully.</p><p>Updated source balance: {money(result.fromBalance)} · Destination balance: {money(result.toBalance)}</p><p>Transfer reference: <code>{result.transferId}</code></p></section>}
        </section></main>;
}
