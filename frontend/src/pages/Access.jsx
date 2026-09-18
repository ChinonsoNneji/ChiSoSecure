import { useEffect, useState } from "react";
import api from "../api";

function Access() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadUsers() {
    try {
      const response = await api.get("/users");
      setUsers(response.data.users ?? response.data ?? []);
    } catch {
      setError("Unable to load users.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadUsers();
  }, []);

  async function updateRole(userId, role) {
    try {
      await api.patch(`/users/${userId}/role`, {
        role,
      });

      setUsers((current) =>
        current.map((user) =>
          user.id === userId
            ? { ...user, role }
            : user
        )
      );
    } catch {
      setError("Unable to update user role.");
    }
  }

  return (
    <main className="main">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Administration</p>
          <h1>Access</h1>
          <p className="page-subtitle">
            Manage ChiSoSecure users and permissions.
          </p>
        </div>
      </div>

      <section className="data-section">
        <div className="data-toolbar">
          <span>{users.length} users</span>
        </div>

        {loading && <p className="state-message">Loading users...</p>}
        {error && <p className="state-message error-text">{error}</p>}

        {!loading && !error && (
          <div className="data-table">
            <div className="data-row data-header users-grid">
              <span>ID</span>
              <span>Username</span>
              <span>Role</span>
              <span>Created</span>
            </div>

            {users.map((user) => (
              <div className="data-row users-grid" key={user.id}>
                <span className="mono">#{user.id}</span>
                <strong>{user.username}</strong>

                <select
                  className="status-select"
                  value={user.role}
                  onChange={(e) =>
                    updateRole(user.id, e.target.value)
                  }
                >
                  <option value="viewer">Viewer</option>
                  <option value="analyst">Analyst</option>
                  <option value="admin">Admin</option>
                </select>

                <span className="muted-cell">
                  {user.created_at
                    ? new Date(user.created_at).toLocaleString()
                    : "—"}
                </span>
              </div>
            ))}

            {users.length === 0 && (
              <div className="empty-state">No users found.</div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}

export default Access;