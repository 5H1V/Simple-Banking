import { useState } from "react";

function UserSearch({ onSearch }) {
    const [userId, setUserId] = useState("");
    const handleSubmit = (event) => {
        event.preventDefault();
        if (!userId.trim()) {
            return;
        }
        onSearch(userId);
    };

    return (
        <div className="search-container">
            <h2>Get User By ID</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={userId}
                    onChange={(event) =>
                        setUserId(event.target.value)
                    }
                    placeholder="Enter User ID"
                />
                <button type="submit">
                    Search
                </button>
            </form>
        </div>
    );
}

export default UserSearch;