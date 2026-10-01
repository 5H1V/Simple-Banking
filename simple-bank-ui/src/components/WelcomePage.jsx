import { Link } from "react-router-dom";

import ThemeToggle from "./common/ThemeToggle";
import "./WelcomePage.css";

function WelcomePage() {
    return (
        <div className="welcome-page">
            <header className="welcome-header">
                <Link className="welcome-brand" to="/">Simple Bank</Link>
                <nav aria-label="Main navigation">
                    <Link to="/login">Sign in</Link>
                    <Link to="/register">Register</Link>
                    <Link to="/accounts">Accounts</Link>
                    <Link to="/transactions">Transactions</Link>
                    <ThemeToggle />
                </nav>
            </header>

            <main className="welcome-main">
                <section className="welcome-hero" aria-labelledby="welcome-title">
                    <p className="welcome-eyebrow">Welcome to Simple Bank</p>
                    <h1 id="welcome-title">Click below to get started</h1>
                    <p className="welcome-description">
                        Manage your accounts, make transactions, and review your banking activity securely.
                    </p>
                    <Link className="welcome-action" to="/register">
                        Open a Customer Account
                    </Link>
                    <Link className="welcome-action" to="/login">
                        Sign In
                    </Link>
                    <Link className="welcome-action" to="/accounts">
                        Create or View Accounts
                    </Link>
                </section>
            </main>
        </div>
    );
}

export default WelcomePage;
