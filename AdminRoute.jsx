import { Navigate } from "react-router-dom";

export default function AdminRoute({ children }) {
  const role = localStorage.getItem("role");

  if (role !== "superadmin") {
    return <Navigate to="/" />;
  }

  return children;
}
