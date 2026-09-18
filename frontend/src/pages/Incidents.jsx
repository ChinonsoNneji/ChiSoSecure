import { useEffect, useState } from "react";
import api from "../api";

function Incidents() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busyId, setBusyId] = useState(null);

  async function loadIncidents() {
    try {
      const response = await api.get("/incidents");

      setIncidents(
        response.data.incidents ??
          response.data ??
          []
      );

      setError("");
    } catch (err) {
      console.error(err);
      setError("Unable to load incidents.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadIncidents();
  }, []);

  async function updateStatus(id, status) {
    try {
      setBusyId(id);
      setError("");

      await api.patch(`/incidents/${id}`, {
        status,
      });

      setIncidents((current) =>
        current.map((incident) =>
          incident.id === id
            ? { ...incident, status }
            : incident
        )
      );
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ??
          "Unable to update incident status."
      );
    } finally {
      setBusyId(null);
    }
  }

  async function runResponseAction(
    incidentId,
    actionType,
    target
  ) {
    try {
      setBusyId(incidentId);
      setError("");

      await api.post("/response-actions", {
        incident_id: incidentId,
        action_type: actionType,
        target,
      });

      alert(
        "Response action executed successfully."
      );
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ??
          "Unable to execute response action."
      );
    } finally {
      setBusyId(null);
    }
  }

  return (
    <main className="main">
      <div className="page-heading">
        <div>
          <p className="eyebrow">
            Case Management
          </p>

          <h1>Incidents</h1>

          <p className="page-subtitle">
            Investigate, respond to, and resolve
            security incidents.
          </p>
        </div>
      </div>

      <section className="data-section">
        <div className="data-toolbar">
          <span>
            {incidents.length} incidents
          </span>
        </div>

        {loading && (
          <p className="state-message">
            Loading incidents...
          </p>
        )}

        {error && (
          <p className="state-message error-text">
            {error}
          </p>
        )}

        {!loading && (
          <div className="incident-cards">
            {incidents.map((incident) => {
              const isResolved =
                incident.status === "resolved";

              const isBusy =
                busyId === incident.id;

              return (
                <article
                  className="incident-card"
                  key={incident.id}
                >
                  <div className="incident-card-top">
                    <div>
                      <span className="incident-id">
                        Incident #{incident.id}
                      </span>

                      <h2>{incident.title}</h2>
                    </div>

                    <span
                      className={`severity severity-${incident.severity?.toLowerCase()}`}
                    >
                      {incident.severity}
                    </span>
                  </div>

                  <div className="incident-meta">
                    <span>
                      Alert #{incident.alert_id}
                    </span>

                    <span>
                      Status:{" "}
                      <strong>
                        {incident.status}
                      </strong>
                    </span>

                    <span>
                      Created:{" "}
                      {incident.created_at
                        ? new Date(
                            incident.created_at
                          ).toLocaleString()
                        : "—"}
                    </span>
                  </div>

                  <div className="incident-controls">
                    <div className="incident-control-group">
                      <span className="control-label">
                        Workflow
                      </span>

                      <button
                        className="secondary-button"
                        disabled={
                          isBusy || isResolved
                        }
                        onClick={() =>
                          updateStatus(
                            incident.id,
                            "investigating"
                          )
                        }
                      >
                        Mark Investigating
                      </button>

                      <button
                        className="secondary-button"
                        disabled={
                          isBusy || isResolved
                        }
                        onClick={() =>
                          updateStatus(
                            incident.id,
                            "resolved"
                          )
                        }
                      >
                        Resolve Incident
                      </button>
                    </div>

                    <div className="incident-control-group">
                      <span className="control-label">
                        Response
                      </span>

                      <button
                        className="response-button"
                        disabled={
                          isBusy || isResolved
                        }
                        onClick={() =>
                          runResponseAction(
                            incident.id,
                            "block_ip",
                            "192.168.77.250"
                          )
                        }
                      >
                        Block IP
                      </button>

                      <button
                        className="response-button"
                        disabled={
                          isBusy || isResolved
                        }
                        onClick={() =>
                          runResponseAction(
                            incident.id,
                            "isolate_host",
                            "workstation-04"
                          )
                        }
                      >
                        Isolate Host
                      </button>

                      <button
                        className="response-button"
                        disabled={
                          isBusy || isResolved
                        }
                        onClick={() =>
                          runResponseAction(
                            incident.id,
                            "disable_account",
                            "svc-backup"
                          )
                        }
                      >
                        Disable Account
                      </button>
                    </div>
                  </div>
                </article>
              );
            })}

            {incidents.length === 0 && (
              <div className="empty-state">
                No incidents found.
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}

export default Incidents;