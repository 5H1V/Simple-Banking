import { Link } from "react-router-dom";
import ThemeToggle from "./common/ThemeToggle";

export default function NotFound() {
    return <main className="not-found"><div className="not-found-top"><Link to="/">Simple Bank</Link><ThemeToggle /></div><h1>Page not found</h1><p>The page you requested does not exist.</p><Link to="/">Return home</Link></main>;
}
