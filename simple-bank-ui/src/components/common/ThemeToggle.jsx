import { useTheme } from "../../context/ThemeContext";

export default function ThemeToggle() {
    const { theme, toggleTheme } = useTheme();
    return <button type="button" className="theme-toggle" onClick={toggleTheme} aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`} title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}>
        <span aria-hidden="true">{theme === "dark" ? "☀" : "☾"}</span> {theme === "dark" ? "Light mode" : "Dark mode"}
    </button>;
}
