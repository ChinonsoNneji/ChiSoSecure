import { useEffect, useState } from "react";
import api from "../api";

function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const [form, setForm] = useState({
    source_ip: "",
    event_type: "failed_login",
    severity: "medium",
    description: "",
  });

  async function loadEvents() {
    try {
      const response = await api.get("/events");

      setEvents(
        response.data.events ??
        response.data ??
        []
      );

      setError("");
    } catch (err) {
      console.error(err);
      setError("Unable to load security events.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadEvents();
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setSubmitting(true);
    setError("");

    try {
      await api.post("/events", form);

      setForm({
        source_ip: "",
        event_type: "failed_login",
        severity: "medium",
        description: "",
      });

      setShowForm(false);

      await loadEvents();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ??
        "Unable to submit security event."
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="main">
      <div className="page-heading page-heading-row">
        <div>
          <p className="eyebrow">Telemetry</p>

          <h1>Events</h1>

          <p className="page-subtitle">
            Raw security activity received by ChiSoSecure.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={() => setShowForm((current) => !current)}
        >
          {showForm ? "Cancel" : "+ Submit Event"}
        </button>
      </div>

      {showForm && (
        <section className="event-form-panel">
          <div className="event-form-heading">
            <div>
              <p className="section-kicker">
                Event ingestion
              </p>

              <h2>Submit security event</h2>
            </div>
          </div>

          <form
            className="event-form"
            onSubmit={handleSubmit}
          >
            <label>
              Source IP

              <input
                name="source_ip"
                value={form.source_ip}
                onChange={handleChange}
                placeholder="192.168.1.50"
                required
              />
            </label>

            <label>
              Event Type

              <select
                name="event_type"
                value={form.event_type}
                onChange={handleChange}
              >
                <option value="failed_login">
                  Failed Login
                </option>

                <option value="malware">
                  Malware
                </option>

                <option value="privilege_escalation">
                  Privilege Escalation
                </option>

                <option value="suspicious_activity">
                  Suspicious Activity
                </option>
              </select>
            </label>

            <label>
              Severity

              <select
                name="severity"
                value={form.severity}
                onChange={handleChange}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </label>

            <label className="description-field">
              Description

              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="Describe what happened..."
                required
              />
            </label>

            <div className="event-form-actions">
              <button
                type="button"
                className="secondary-button"
                onClick={() => setShowForm(false)}
              >
                Cancel
              </button>

              <button
                type="submit"
                className="primary-button"
                disabled={submitting}
              >
                {submitting
                  ? "Submitting..."
                  : "Submit Event"}
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="data-section">
        <div className="data-toolbar">
          <span>{events.length} events</span>
        </div>

        {loading && (
          <p className="state-message">
            Loading events...
          </p>
        )}

        {error && (
          <p className="state-message error-text">
            {error}
          </p>
        )}

        {!loading && (
          <div className="data-table">
            <div className="data-row data-header events-grid">
              <span>ID</span>
              <span>Source</span>
              <span>Type</span>
              <span>Severity</span>
              <span>Description</span>
              <span>Created</span>
            </div>

            {events.map((event) => (
              <div
                className="data-row events-grid"
                key={event.id}
              >
                <span className="mono">
                  #{event.id}
                </span>

                <span className="mono">
                  {event.source_ip}
                </span>

                <strong>
                  {event.event_type}
                </strong>

                <span>
                  <span
                    className={`severity severity-${event.severity?.toLowerCase()}`}
                  >
                    {event.severity}
                  </span>
                </span>

                <span>
                  {event.description}
                </span>

                <span className="muted-cell">
                  {event.created_at
                    ? new Date(event.created_at).toLocaleString()
                    : "—"}
                </span>
              </div>
            ))}

            {events.length === 0 && (
              <div className="empty-state">
                No security events found.
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}

export default Events;