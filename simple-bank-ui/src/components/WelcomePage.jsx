import { Link } from "react-router-dom";

import "./WelcomePage.css";

function WelcomePage() {
    return (
        <div className="welcome-page">
            <header className="welcome-header">
                <Link className="welcome-brand" to="/">Simple Bank</Link>
                <nav aria-label="Main navigation">
                    <Link to="/users">User Management</Link>
                    <Link to="/accounts">Accounts</Link>
                    <Link to="/transactions">Deposit / Withdraw</Link>
                </nav>
            </header>

            <main className="welcome-main">
                <section className="welcome-hero" aria-labelledby="welcome-title">
                    <p className="welcome-eyebrow">Welcome to Simple Bank</p>
                    <h1 id="welcome-title">Click below to get started</h1>
                    <p className="welcome-description">
                        Find, add, and update user records in one place.
                    </p>
                    <Link className="welcome-action" to="/users">
                        Go to User Management
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
