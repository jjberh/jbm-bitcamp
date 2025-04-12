import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);  // to show loading state
  const [error, setError] = useState(null);      // to handle fetch errors

  useEffect(() => {
    fetch("https://jbm-bitcamp.onrender.com/users")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Network response was not ok");
        }
        return res.json();
      })
      .then((data) => {
        setUsers(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <div className="whole-page">

      <h1>Project</h1>

      {loading && <p>Loading users...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {!loading && users.length === 0 && <p>No users found.</p>}

      {!loading && users.length > 0 && (
        <div>
          <h2>User List</h2>
          {users.map((user) => (
            <div key={user.id} className="user-card">
              <p><strong>Username:</strong> {user.username}</p>
              <p><strong>Email:</strong> {user.email}</p>
            </div>
            
          ))}
        </div>
      )}
    </div>
    </div>
    
  );
}

export default App;
