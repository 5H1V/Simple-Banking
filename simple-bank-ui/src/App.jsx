import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import UserForm from "./components/UserForm";
import UserList from "./components/UserList";
import UserSearch from "./components/UserSearch";

import {
    getAllUsers,
    getUserById,
    createUser,
    updateUser,
    deleteUser
} from "./services/userApi";

import "./App.css";

function App() {
    const [users, setUsers] = useState([]);
    const [selectedUser, setSelectedUser] = useState(null);
    const [searchedUser, setSearchedUser] = useState(null);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    // -----------------------------
    // GET ALL USERS
    // -----------------------------
    const loadUsers = async () => {
        try {
            setError("");
            const data = await getAllUsers();
            setUsers(data);
        } catch (error) {
            setError(error.message);
        }
    };

    // Load users when application starts
    useEffect(() => {
        loadUsers();
    }, []);

    // -----------------------------
    // CREATE / UPDATE USER
    // -----------------------------
    const handleSubmit = async (userData) => {

        try {

            setError("");
            setMessage("");

            if (selectedUser) {

                await updateUser(
                    selectedUser.userId,
                    userData
                );

                setMessage(
                    "User updated successfully."
                );

                setSelectedUser(null);

            } else {

                await createUser(userData);

                setMessage(
                    "User created successfully."
                );
            }

            await loadUsers();

        } catch (error) {

            setError(error.message);
        }
    };

    // -----------------------------
    // DELETE USER
    // -----------------------------
    const handleDelete = async (userId) => {

        const confirmed = window.confirm(
            "Are you sure you want to delete this user?"
        );

        if (!confirmed) {
            return;
        }

        try {

            setError("");
            setMessage("");

            await deleteUser(userId);

            setMessage(
                "User deleted successfully."
            );

            await loadUsers();

        } catch (error) {

            setError(error.message);
        }
    };

    // -----------------------------
    // GET USER BY ID
    // -----------------------------
    const handleSearch = async (userId) => {

        try {

            setError("");
            setSearchedUser(null);

            const user =
                await getUserById(userId);

            setSearchedUser(user);

        } catch (error) {

            setError(error.message);
        }
    };


    return (

        <div className="app">

            <header>

                <h1>
                    Simple Bank
                </h1>

                <p>
                    User Management
                </p>

                <nav aria-label="Main navigation">
                    <Link to="/">Home</Link>
                    {" | "}
                    <Link to="/accounts">Accounts</Link>
                    {" | "}
                    <Link to="/transactions">Deposit / Withdraw</Link>
                </nav>

            </header>


            {message && (

                <div className="success-message">
                    {message}
                </div>

            )}


            {error && (

                <div className="error-message">
                    {error}
                </div>

            )}


            <main>

                {/* Add / Edit */}

                <UserForm
                    selectedUser={selectedUser}
                    onSubmit={handleSubmit}
                    onCancel={() =>
                        setSelectedUser(null)
                    }
                />


                {/* Search */}

                <UserSearch
                    onSearch={handleSearch}
                />


                {/* Search Result */}

                {searchedUser && (

                    <div className="search-result">

                        <h2>
                            User Found
                        </h2>

                        <p>
                            <strong>ID:</strong>{" "}
                            {searchedUser.userId}
                        </p>

                        <p>
                            <strong>Name:</strong>{" "}
                            {searchedUser.name}
                        </p>

                        <p>
                            <strong>Email:</strong>{" "}
                            {searchedUser.email}
                        </p>

                    </div>

                )}


                {/* All Users */}

                <UserList
                    users={users}
                    onEdit={setSelectedUser}
                    onDelete={handleDelete}
                />

            </main>

        </div>
    );
}

export default App;