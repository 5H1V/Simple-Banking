export default function LoadingState({ message = "Loading...", className = "" }) {
    return (
        <p className={className} role="status">
            {message}
        </p>
    );
}