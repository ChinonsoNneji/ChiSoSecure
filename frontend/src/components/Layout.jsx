import {
    NavLink,
    Outlet,
    useNavigate,
  } from "react-router-dom";
  
  import {
    LogOut,
    Shield,
  } from "lucide-react";
  
  
  function Layout() {
    const navigate = useNavigate();
  
    function logout() {
      localStorage.removeItem("chisosecure_token");
      localStorage.removeItem("chisosecure_user");
      navigate("/login");
    }
  
    return (
      <div className="app">
        <header className="top-shell">
          <div className="brand-row">
            <div className="brand-left">
              <div className="brand-icon">
                <Shield size={18} strokeWidth={2} />
              </div>
  
              <div>
                <div className="brand-name">
                  ChiSoSecure
                </div>
  
                <div className="brand-tagline">
                  Security Operations
                </div>
              </div>
            </div>
  
            <div className="top-right">
              <div className="live-indicator">
                <span className="live-dot" />
                SYSTEM ONLINE
              </div>
  
              <div className="analyst">
                <div className="analyst-copy">
                  <strong>Nonso Nneji</strong>
                  <span>Administrator</span>
                </div>
  
                <div className="avatar">
                  NN
                </div>
              </div>
  
              <button
                className="logout-icon"
                onClick={logout}
                title="Log out"
              >
                <LogOut size={16} />
              </button>
            </div>
          </div>
  
          <nav className="top-nav">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              Operations
            </NavLink>
  
            <NavLink
              to="/events"
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              Events
            </NavLink>
  
            <NavLink
              to="/alerts"
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              Alerts
            </NavLink>
  
            <NavLink
              to="/incidents"
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              Incidents
            </NavLink>
  
            <NavLink
              to="/actions"
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              Actions
            </NavLink>
  
            <NavLink
              to="/access"
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              Access
            </NavLink>
          </nav>
        </header>
  
        <Outlet />
      </div>
    );
  }
  
  
  export default Layout;