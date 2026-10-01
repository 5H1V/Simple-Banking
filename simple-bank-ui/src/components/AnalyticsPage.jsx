import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getMyCashFlow } from "../services/accountApi";
import ThemeToggle from "./common/ThemeToggle";
import LoadingState from "./common/LoadingState";
import ErrorMessage from "./common/ErrorMessage";
import "./FeaturePages.css";

const money = value => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(Number(value || 0));

function CashFlowChart({ rows }) {
    const max = Math.max(1, ...rows.flatMap(row => [row.deposits || 0, row.withdrawals || 0]));
    if (!rows.length) return <p className="empty-chart">No deposit or withdrawal activity was found in this date range.</p>;
    return <div className="bar-chart" role="img" aria-label="Monthly deposits compared with withdrawals across all owned accounts">{rows.map(row => <div className="bar-group" key={row.month}><div className="bars"><div className="bar bar-deposit" style={{ height: `${Math.max(2, (row.deposits / max) * 170)}px` }} title={`Deposits: ${money(row.deposits)}`} /><div className="bar bar-withdrawal" style={{ height: `${Math.max(2, (row.withdrawals / max) * 170)}px` }} title={`Withdrawals: ${money(row.withdrawals)}`} /></div><span className="bar-label">{row.month}</span><span className="bar-values">{money(row.deposits)} / {money(row.withdrawals)}</span></div>)}</div>;
}

export default function AnalyticsPage() {
    const [days, setDays] = useState("90");
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const load = useCallback(async () => { setLoading(true); setError(""); try { setData(await getMyCashFlow(Number(days))); } catch (e) { setError(e.message); } finally { setLoading(false); } }, [days]);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    useEffect(() => { load(); }, [load]);
    const totals = data?.totals || {};
    return <main className="feature-page"><header className="feature-header"><Link className="feature-brand" to="/dashboard">Simple Bank</Link><nav><Link to="/dashboard">Dashboard</Link><Link to="/accounts">Accounts</Link><Link to="/transfers">Transfers</Link><Link to="/transactions">Deposit / Withdraw</Link><ThemeToggle /></nav></header>
        <section className="feature-main analytics-main"><p className="eyebrow">YOUR MONEY, AT A GLANCE</p><h1>Cash flow analytics</h1><p className="feature-intro">A consolidated view of deposits and withdrawals across all of your accounts. Internal transfers are reported separately.</p>
            <div className="filter-row"><label htmlFor="analytics-days">Date range</label><select id="analytics-days" value={days} onChange={e => setDays(e.target.value)}><option value="30">Last 30 days</option><option value="90">Last 90 days</option><option value="180">Last 180 days</option><option value="365">Last 12 months</option></select></div>
            {error && <ErrorMessage message={error} onRetry={load} />}
            {loading ? <LoadingState message="Calculating cash flow…" /> : <><div className="metric-grid"><article className="metric-card"><span>Total deposits</span><strong className="metric-positive">{money(totals.deposits)}</strong></article><article className="metric-card"><span>Total withdrawals</span><strong>{money(totals.withdrawals)}</strong></article><article className="metric-card"><span>Net external cash flow</span><strong>{money(data?.netExternalCashFlow)}</strong></article><article className="metric-card"><span>Internal transfers in / out</span><strong>{money(totals.transfersIn)} / {money(totals.transfersOut)}</strong></article></div>
                <section className="feature-card"><div className="chart-heading"><div><h2>Deposits vs. withdrawals</h2><p>Monthly totals · {data?.accountCount || 0} owned accounts included</p></div><div className="chart-legend"><span><i className="legend-deposit" /> Deposits</span><span><i className="legend-withdrawal" /> Withdrawals</span></div></div><CashFlowChart rows={data?.monthly || []} /></section>
                <section className="feature-card"><h2>Monthly breakdown</h2>{!data?.monthly?.length ? <p className="muted">No activity in this period.</p> : <div className="table-wrap"><table><thead><tr><th>Month</th><th>Deposits</th><th>Withdrawals</th><th>Net cash flow</th><th>Transfers in / out</th></tr></thead><tbody>{data.monthly.map(row => <tr key={row.month}><td>{row.month}</td><td>{money(row.deposits)}</td><td>{money(row.withdrawals)}</td><td>{money(row.deposits - row.withdrawals)}</td><td>{money(row.transfersIn)} / {money(row.transfersOut)}</td></tr>)}</tbody></table></div>}</section>
            </>}
        </section></main>;
}
