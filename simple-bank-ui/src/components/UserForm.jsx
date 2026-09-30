import { useEffect, useState } from "react";

function UserForm({
    selectedUser,
    onSubmit,
    onCancel
}) {

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");

    useEffect(() => {

        if (selectedUser) {
            setName(selectedUser.name);
            setEmail(selectedUser.email);
        } else {
            setName("");
            setEmail("");
        }

    }, [selectedUser]);


    const handleSubmit = (event) => {

        event.preventDefault();

        onSubmit({
            name,
            email
        });
    };


    return (
        <div className="form-container">

            <h2>
                {selectedUser
                    ? "Edit User"
                    : "Add User"}
            </h2>

            <form onSubmit={handleSubmit}>

                <div className="form-group">
                    <label>Name</label>

                    <input
                        type="text"
                        value={name}
                        onChange={(event) =>
                            setName(event.target.value)
                        }
                        placeholder="Enter name"
                        required
                    />
                </div>


                <div className="form-group">
                    <label>Email</label>

                    <input
                        type="email"
                        value={email}
                        onChange={(event) =>
                            setEmail(event.target.value)
                        }
                        placeholder="Enter email"
                        required
                    />
                </div>


                <div className="form-buttons">

                    <button type="submit">
                        {selectedUser
                            ? "Update User"
                            : "Add User"}
                    </button>

                    {selectedUser && (
                        <button
                            type="button"
                            onClick={onCancel}
                        >
                            Cancel
                        </button>
                    )}

                </div>

            </form>

        </div>
    );
}

export default UserForm;