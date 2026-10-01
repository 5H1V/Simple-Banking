import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getAdminFraudAlerts, reviewAdminFraudAlert } from "../services/accountApi";
import ThemeToggle from "./common/ThemeToggle";
import LoadingState from "./common/LoadingState";
import ErrorMessage from "./common/ErrorMessage";
import "./FeaturePages.css";

const money = value => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(Number(value || 0));
const date = value => value ? new Date(value).toLocaleString() : "Date unavailable";

export default function FraudAlertsPage() {
    const [alerts, setAlerts] = useState([]);
    const [statusFilter, setStatusFilter] = useState("all");
    const [severityFilter, setSeverityFilter] = useState("all");
    const [methodFilter, setMethodFilter] = useState("all");
    const [dateFilter, setDateFilter] = useState("all");
    const [dateCutoff, setDateCutoff] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [busyId, setBusyId] = useState("");
    const [notes, setNotes] = useState({});
    const load = useCallback(async () => { setLoading(true); setError(""); try { setAlerts(await getAdminFraudAlerts()); } catch (e) { setError(e.message); } finally { setLoading(false); } }, []);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    useEffect(() => { load(); }, [load]);
    async function review(alert, status) {
        setBusyId(alert.alertId); setError("");
        try { const updated = await reviewAdminFraudAlert(alert.alertId, status, notes[alert.alertId] || ""); setAlerts(current => current.map(item => item.alertId === updated.alertId ? updated : item)); }
        catch (e) { setError(e.message); }
        finally { setBusyId(""); }
    }
    const visible = alerts.filter(alert => {
        if (statusFilter !== "all" && alert.reviewStatus !== statusFilter) return false;
        const score = Number(alert.riskScore || 0);
        if (severityFilter === "high" && score < 0.75) return false;
        if (severityFilter === "medium" && (score < 0.5 || score >= 0.75)) return false;
        if (severityFilter === "low" && score >= 0.5) return false;
        if (methodFilter !== "all" && !(alert.detectionMethods || []).includes(methodFilter)) return false;
        if (dateFilter !== "all" && alert.createdAt && new Date(alert.createdAt).getTime() < dateCutoff) return false;
        return true;
    });
    const pending = alerts.filter(alert => alert.reviewStatus === "pending").length;
    return <main className="feature-page"><header className="feature-header"><Link className="feature-brand" to="/admin/dashboard">Simple Bank Admin</Link><nav><Link to="/admin/dashboard">Dashboard</Link><Link to="/users">User Management</Link><Link to="/accounts">Accounts</Link><Link to="/admin/fraud-alerts">Fraud monitoring</Link><ThemeToggle /></nav></header>
        <section className="feature-main analytics-main"><p className="eyebrow">ADMINISTRATOR ONLY</p><h1>Fraud & anomaly monitoring</h1><p className="feature-intro">Review transactions flagged by transparent rules and an Isolation Forest anomaly-detection prototype. Flags indicate unusual behavior, not proof of fraud.</p>
            <div className="metric-grid"><article className="metric-card"><span>Total alerts</span><strong>{alerts.length}</strong></article><article className="metric-card"><span>Awaiting review</span><strong>{pending}</strong></article><article className="metric-card"><span>Confirmed suspicious</span><strong>{alerts.filter(a => a.reviewStatus === "confirmed_suspicious").length}</strong></article><article className="metric-card"><span>Marked false positive</span><strong>{alerts.filter(a => a.reviewStatus === "false_positive").length}</strong></article></div>
            <div className="filter-row"><label htmlFor="alert-status">Review status</label><select id="alert-status" value={statusFilter} onChange={e => setStatusFilter(e.target.value)}><option value="all">All statuses</option><option value="pending">Pending</option><option value="reviewed">Reviewed</option><option value="confirmed_suspicious">Confirmed suspicious</option><option value="false_positive">False positive</option></select><label htmlFor="alert-severity">Severity</label><select id="alert-severity" value={severityFilter} onChange={e => setSeverityFilter(e.target.value)}><option value="all">All severity</option><option value="high">High (75+)</option><option value="medium">Medium (50–74)</option><option value="low">Low (under 50)</option></select><label htmlFor="alert-method">Detection</label><select id="alert-method" value={methodFilter} onChange={e => setMethodFilter(e.target.value)}><option value="all">All methods</option><option value="rules">Rules</option><option value="isolation_forest">Isolation Forest</option></select><label htmlFor="alert-date">Date range</label><select id="alert-date" value={dateFilter} onChange={e => { const value = e.target.value; setDateFilter(value); setDateCutoff(value === "all" ? 0 : Date.now() - Number(value) * 86400000); }}><option value="all">All dates</option><option value="7">Last 7 days</option><option value="30">Last 30 days</option><option value="90">Last 90 days</option></select><button type="button" onClick={load} disabled={loading}>Refresh analysis</button></div>
            {error && <ErrorMessage message={error} onRetry={load} />}
            {loading ? <LoadingState message="Analyzing transaction patterns…" /> : !visible.length ? <section className="feature-card"><h2>No alerts in this view</h2><p>Refresh analysis to scan the current transaction history again.</p></section> : <div className="alert-list">{visible.map(alert => <article className="feature-card alert-card" key={alert.alertId}><div className="alert-heading"><div><span className={`status-pill status-${alert.reviewStatus}`}>{alert.reviewStatus.replaceAll("_", " ")}</span><h2>{alert.transactionType} · {money(alert.amount)}</h2><p>{date(alert.createdAt)}</p></div><div className="risk-score"><span>Risk score</span><strong>{Math.round(alert.riskScore * 100)} / 100</strong></div></div><dl className="alert-details"><div><dt>Transaction ID</dt><dd>{alert.transactionId}</dd></div><div><dt>Account ID</dt><dd>{alert.accountId}</dd></div><div><dt>User ID</dt><dd>{alert.userId}</dd></div><div><dt>Detection model</dt><dd>{alert.modelVersion}</dd></div></dl><h3>Why it was flagged</h3><ul className="reason-list">{alert.reasons.map(reason => <li key={reason}>{reason}</li>)}</ul>{alert.detectionMethods?.length > 0 && <p className="method-line">Methods: {alert.detectionMethods.join(", ")}</p>}
                    <label htmlFor={`note-${alert.alertId}`}>Review note</label><textarea id={`note-${alert.alertId}`} rows="2" maxLength="1000" value={notes[alert.alertId] ?? alert.reviewNote ?? ""} onChange={e => setNotes(current => ({ ...current, [alert.alertId]: e.target.value }))} placeholder="Optional note for the audit trail" />
                    <div className="alert-actions"><button type="button" onClick={() => review(alert, "reviewed")} disabled={busyId === alert.alertId}>Mark reviewed</button><button type="button" className="button-warning" onClick={() => review(alert, "confirmed_suspicious")} disabled={busyId === alert.alertId}>Confirm suspicious</button><button type="button" className="button-secondary" onClick={() => review(alert, "false_positive")} disabled={busyId === alert.alertId}>False positive</button></div>
                </article>)}</div>}
            <p className="feature-note">This prototype does not automatically block transactions or freeze accounts. ML scores are experimental and should be evaluated before being used for real financial decisions.</p>
        </section></main>;
}
