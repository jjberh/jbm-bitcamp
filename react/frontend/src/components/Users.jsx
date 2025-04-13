import { useEffect, useState } from "react";

function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("https://your-backend.onrender.com/users")
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => console.error("Error fetching users:", err));
  }, []);

  return (
    <div>
      <h2>User List</h2>
      {users.map(user => (
        <div key={user.id}>
          <p><strong>Username:</strong> {user.username}</p>
          <input type='text' placeholder="Enter Username" onChange={(e) => setDate(e.target.value)}/>
          <p><strong>Email:</strong> {user.email}</p>
          <input type='text' placeholder="Enter Email" onChange={(e) => setDate(e.target.value)}/>

        </div>
      ))}
    </div>
  );
}

export default Users;