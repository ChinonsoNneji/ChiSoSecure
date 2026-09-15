import { useEffect, useState } from "react";
import api from "../api";

function Actions() {
  const [actions, setActions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadActions() {
      try {
        const response = await api.get("/response-actions");

        setActions(
          response.data.actions ??
          response.data.response_actions ??
          response.data ??
          []
        );
      } catch {
        setError("Unable to load response actions.");
      } finally {
        setLoading(false);
      }
    }

    loadActions();
  }, []);

  return (
    <main className="main">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Automation</p>
          <h1>Response Actions</h1>
          <p className="page-subtitle">
            Security actions executed against active incidents.
          </p>
        </div>
      </div>

      <section className="data-section">
        <div className="data-toolbar">
          <span>{actions.length} actions</span>
        </div>

        {loading && <p className="state-message">Loading actions...</p>}
        {error && <p className="state-message error-text">{error}</p>}

        {!loading && !error && (
          <div className="data-table">
            <div className="data-row data-header actions-grid">
              <span>ID</span>
              <span>Incident</span>
              <span>Action</span>
              <span>Target</span>
              <span>Status</span>
              <span>Result</span>
              <span>Created</span>
            </div>

            {actions.map((action) => (
              <div className="data-row actions-grid" key={action.id}>
                <span className="mono">#{action.id}</span>
                <span className="mono">#{action.incident_id}</span>
                <strong>{action.action_type}</strong>
                <span className="mono">{action.target}</span>

                <span>
                  <span className={`status status-${action.status?.toLowerCase()}`}>
                    {action.status}
                  </span>
                </span>

                <span>{action.result}</span>

                <span className="muted-cell">
                  {action.created_at
                    ? new Date(action.created_at).toLocaleString()
                    : "—"}
                </span>
              </div>
            ))}

            {actions.length === 0 && (
              <div className="empty-state">
                No response actions found.
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}

export default Actions;