export default function ErrorMessage({
    message,
    onRetry,
    retryLabel = "Retry",
    disabled = false,
    className = ""
}) {
    return (
        <div className={className} role="alert">
            <span>{message}</span>
            {onRetry && (
                <button type="button" onClick={onRetry} disabled={disabled}>
                    {retryLabel}
                </button>
            )}
        </div>
    );
}