import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  Bell,
  ChevronRight,
  CircleDot,
  Users,
  Zap,
} from "lucide-react";

import api from "../api";


function Severity({ value }) {
  const safeValue = value || "unknown";

  return (
    <span
      className={`severity severity-${safeValue.toLowerCase()}`}
    >
      {safeValue}
    </span>
  );
}


function Status({ value }) {
  const safeValue = value || "unknown";

  return (
    <span
      className={`status status-${safeValue.toLowerCase()}`}
    >
      {safeValue}
    </span>
  );
}


function formatTime(value) {
  if (!value) {
    return "—";
  }

  return new Date(value).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}


function Operations() {
  const [events, setEvents] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [actions, setActions] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    async function loadDashboard() {
      try {
        const [
          eventsResponse,
          alertsResponse,
          incidentsResponse,
          actionsResponse,
        ] = await Promise.all([
          api.get("/events"),
          api.get("/alerts"),
          api.get("/incidents"),
          api.get("/response-actions"),
        ]);

        setEvents(
          eventsResponse.data.events ??
          eventsResponse.data ??
          []
        );

        setAlerts(
          alertsResponse.data.alerts ??
          alertsResponse.data ??
          []
        );

        setIncidents(
          incidentsResponse.data.incidents ??
          incidentsResponse.data ??
          []
        );

        setActions(
          actionsResponse.data.actions ??
          actionsResponse.data.response_actions ??
          actionsResponse.data ??
          []
        );
      } catch (err) {
        console.error(err);
        setError("Unable to load security operations data.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);


  const openIncidents = useMemo(
    () =>
      incidents.filter(
        (incident) =>
          incident.status !== "resolved"
      ),
    [incidents]
  );


  const criticalAlerts = useMemo(
    () =>
      alerts.filter(
        (alert) =>
          alert.severity?.toLowerCase() === "critical"
      ),
    [alerts]
  );


  const latestAlerts = useMemo(
    () =>
      [...alerts]
        .sort(
          (a, b) =>
            new Date(b.created_at || 0) -
            new Date(a.created_at || 0)
        )
        .slice(0, 5),
    [alerts]
  );


  const activeIncidents = useMemo(
    () =>
      [...openIncidents]
        .sort(
          (a, b) =>
            new Date(b.created_at || 0) -
            new Date(a.created_at || 0)
        )
        .slice(0, 4),
    [openIncidents]
  );


  const recentActions = useMemo(
    () =>
      [...actions]
        .sort(
          (a, b) =>
            new Date(b.created_at || 0) -
            new Date(a.created_at || 0)
        )
        .slice(0, 4),
    [actions]
  );


  if (loading) {
    return (
      <main className="main">
        <p className="state-message">
          Loading security operations...
        </p>
      </main>
    );
  }


  if (error) {
    return (
      <main className="main">
        <p className="state-message error-text">
          {error}
        </p>
      </main>
    );
  }


  return (
    <main className="main">
      <section className="page-heading">
        <div>
          <p className="eyebrow">
            Operations Center
          </p>

          <h1>Security activity</h1>

          <p className="page-subtitle">
            Live detection, incident, and response activity
            from ChiSoSecure.
          </p>
        </div>
      </section>


      <section className="status-strip">
        <div className="status-metric">
          <span>Events</span>
          <strong>{events.length}</strong>
        </div>

        <div className="status-metric">
          <span>Alerts</span>
          <strong>{alerts.length}</strong>
        </div>

        <div className="status-metric">
          <span>Open incidents</span>
          <strong>{openIncidents.length}</strong>
        </div>

        <div className="status-metric">
          <span>Critical</span>
          <strong>{criticalAlerts.length}</strong>
        </div>

        <div className="status-metric">
          <span>Automations</span>
          <strong>{actions.length}</strong>
        </div>
      </section>


      <section className="workspace">
        <div className="activity-column">
          <div className="section-heading">
            <div>
              <p className="section-kicker">
                Detection feed
              </p>

              <h2>Latest activity</h2>
            </div>

            <a
              className="link-button"
              href="/alerts"
            >
              View all
              <ChevronRight size={14} />
            </a>
          </div>


          <div className="feed">
            {latestAlerts.map((alert) => (
              <div
                className="feed-row"
                key={alert.id}
              >
                <div className="feed-time">
                  {formatTime(alert.created_at)}
                </div>

                <div className="feed-icon">
                  <CircleDot size={15} />
                </div>

                <div className="feed-copy">
                  <div className="feed-title">
                    {alert.rule_name}
                  </div>

                  <div className="feed-detail">
                    {alert.message}
                  </div>
                </div>

                <Severity value={alert.severity} />
              </div>
            ))}

            {latestAlerts.length === 0 && (
              <div className="empty-state">
                No alerts have been generated yet.
              </div>
            )}
          </div>


          <div className="response-block">
            <div className="section-heading compact">
              <div>
                <p className="section-kicker">
                  Automation
                </p>

                <h2>Recent response activity</h2>
              </div>

              <Zap size={17} />
            </div>


            <div className="response-table">
              <div className="response-header">
                <span>Action</span>
                <span>Target</span>
                <span>Result</span>
                <span>Time</span>
              </div>

              {recentActions.map((action) => (
                <div
                  className="response-row"
                  key={action.id}
                >
                  <strong>
                    {action.action_type}
                  </strong>

                  <span className="mono">
                    {action.target}
                  </span>

                  <span>
                    {action.status}
                  </span>

                  <span>
                    {formatTime(action.created_at)}
                  </span>
                </div>
              ))}

              {recentActions.length === 0 && (
                <div className="empty-state">
                  No response actions recorded.
                </div>
              )}
            </div>
          </div>
        </div>


        <aside className="incident-rail">
          <div className="section-heading rail-heading">
            <div>
              <p className="section-kicker">
                Incidents
              </p>

              <h2>Needs attention</h2>
            </div>

            <AlertTriangle size={17} />
          </div>


          <div className="incident-list">
            {activeIncidents.map((incident) => (
              <a
                className="incident-item"
                key={incident.id}
                href="/incidents"
              >
                <div className="incident-top">
                  <span className="incident-id">
                    #{incident.id}
                  </span>

                  <Severity
                    value={incident.severity}
                  />
                </div>

                <div className="incident-title">
                  {incident.title}
                </div>

                <div className="incident-bottom">
                  <Status
                    value={incident.status}
                  />

                  <ChevronRight size={15} />
                </div>
              </a>
            ))}

            {activeIncidents.length === 0 && (
              <div className="empty-state">
                No active incidents.
              </div>
            )}
          </div>


          <div className="rail-footer">
            <div className="rail-stat">
              <Activity size={15} />
              <span>
                {alerts.length} total alerts
              </span>
            </div>

            <div className="rail-stat">
              <Bell size={15} />
              <span>
                {criticalAlerts.length} critical
              </span>
            </div>

            <div className="rail-stat">
              <Users size={15} />
              <span>Authenticated analyst</span>
            </div>
          </div>
        </aside>
      </section>
    </main>
  );
}


export default Operations; 