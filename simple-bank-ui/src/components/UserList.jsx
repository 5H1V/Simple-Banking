function UserList({
    users,
    onEdit,
    onDelete
}) {

    return (
        <div className="user-list">

            <h2>All Users</h2>

            {users.length === 0 ? (

                <p>No users found.</p>

            ) : (

                <table>

                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>

                        {users.map((user) => (

                            <tr key={user.userId}>

                                <td>
                                    {user.userId}
                                </td>

                                <td>
                                    {user.name}
                                </td>

                                <td>
                                    {user.email}
                                </td>

                                <td>

                                    <button
                                        onClick={() =>
                                            onEdit(user)
                                        }
                                    >
                                        Edit
                                    </button>

                                    <button
                                        onClick={() =>
                                            onDelete(user.userId)
                                        }
                                    >
                                        Delete
                                    </button>

                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            )}

        </div>
    );
}

export default UserList;