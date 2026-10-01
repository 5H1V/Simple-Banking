import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { loginAdmin, loginCustomer, registerCustomer, setupAdmin } from "../services/authApi";
import { getRole } from "../services/apiClient";
import "./AuthPage.css";

export default function AuthPage({ mode = "login" }) {
    const [kind, setKind] = useState("customer");
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [setupKey, setSetupKey] = useState("");
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const location = useLocation();
    const isRegister = mode === "register";
    const isSetup = mode === "admin-setup";

    async function handleSubmit(event) {
        event.preventDefault(); setError(""); setBusy(true);
        try {
            if (isSetup) await setupAdmin({ name, email, password, setupKey });
            else if (isRegister) await registerCustomer({ name, email, password });
            else if (kind === "admin") await loginAdmin({ email, password });
            else await loginCustomer({ email, password });
            navigate(getRole() === "AdminToken" ? "/admin/dashboard" : (location.state?.from?.pathname || "/dashboard"), { replace: true });
        } catch (e) { setError(e.message); }
        finally { setBusy(false); }
    }

    return <main className="auth-shell">
        <Link className="auth-brand" to="/">Simple Bank</Link>
        <section className="auth-card">
            <p className="auth-kicker">SECURE BANKING PORTAL</p>
            <h1>{isSetup ? "Set up the administrator" : isRegister ? "Create your account" : "Welcome back"}</h1>
            <p className="auth-subtitle">{isSetup ? "One-time setup. Protect your setup key and do not share it." : isRegister ? "Register to manage your own accounts." : "Sign in to access your banking dashboard."}</p>
            {!isRegister && !isSetup && <div className="auth-tabs"><button type="button" className={kind === "customer" ? "active" : ""} onClick={() => setKind("customer")}>Customer login</button><button type="button" className={kind === "admin" ? "active" : ""} onClick={() => setKind("admin")}>Admin login</button></div>}
            <form onSubmit={handleSubmit} className="auth-form">
                {(isRegister || isSetup) && <><label htmlFor="auth-name">Full name</label><input id="auth-name" value={name} onChange={e => setName(e.target.value)} required minLength={1} maxLength={100} autoComplete="name" /></>}
                <label htmlFor="auth-email">Email address</label><input id="auth-email" type="email" value={email} onChange={e => setEmail(e.target.value)} required autoComplete="email" />
                <label htmlFor="auth-password">Password</label><input id="auth-password" type="password" value={password} onChange={e => setPassword(e.target.value)} required minLength={isRegister || isSetup ? 10 : 1} autoComplete={isRegister || isSetup ? "new-password" : "current-password"} />
                {isSetup && <><label htmlFor="setup-key">One-time setup key</label><input id="setup-key" type="password" value={setupKey} onChange={e => setSetupKey(e.target.value)} required autoComplete="off" /></>}
                {error && <p className="auth-error" role="alert">{error}</p>}
                <button className="auth-submit" disabled={busy}>{busy ? "Please wait…" : isSetup ? "Create administrator" : isRegister ? "Create customer account" : "Sign in"}</button>
            </form>
            <div className="auth-links">{!isSetup && !isRegister && <p>New customer? <Link to="/register">Register here</Link></p>}{!isSetup && <p><Link to="/admin/setup">First-time administrator setup</Link></p>}{(isSetup || isRegister) && <p>Already registered? <Link to="/login">Sign in</Link></p>}</div>
        </section>
    </main>;
}
