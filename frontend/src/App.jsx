import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";


import Layout from "./components/Layout";
import Access from "./pages/Access";
import Actions from "./pages/Actions";
import Alerts from "./pages/Alerts";
import Events from "./pages/Events";
import Incidents from "./pages/Incidents";
import Login from "./pages/Login";
import Operations from "./pages/Operations";

import "./App.css";


function ProtectedRoute({ children }) {
  const token = localStorage.getItem("chisosecure_token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Operations />} />
          <Route path="events" element={<Events />} />
          <Route path="alerts" element={<Alerts />} />
          <Route path="incidents" element={<Incidents />} />
          <Route path="actions" element={<Actions />} />
          <Route path="access" element={<Access />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;