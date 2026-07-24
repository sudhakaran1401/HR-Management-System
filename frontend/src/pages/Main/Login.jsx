import { useState } from "react";
import AlertMessage from "../../components/AlertMessage";
import api from "../../services/api";
import useAlert from "../../hooks/useAlert";
import Navbar from "../../components/Navbar";

function Login() {
  const { alert, showAlert, closeAlert } = useAlert();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Login
      const response = await api.post("/api/token/", {
        username,
        password,
      });

      const access = response.data.access;
      const refresh = response.data.refresh;

      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);

      // Get logged-in user
      const userRes = await api.get("/api/me/", {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      });

      const userId = userRes.data.id;

      // Get all employees
      const empRes = await api.get("/api/employees/", {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      });

      // Find employee linked to logged-in user
      const employee = empRes.data.find(
        (emp) => emp.user === userId
      );

      if (!employee) {

        showAlert("danger", "Employee profile not found.");
        return;
      }

      // Save employee details
      localStorage.setItem("employee", JSON.stringify(employee));

      sessionStorage.setItem(
          "alert",
          JSON.stringify({
            type: "success",
            message: "Login successful.",
          })
        );

      setTimeout(() => {
        if (employee.department === "HR") {
          window.location.href = "/hr/dashboard";
        } else {
          window.location.href = "/me/dashboard";
        }
      }, 1500);


    } catch (error) {
      console.error(error);
      showAlert("danger", "Invalid Credentials.");
    }
  };

  return (
  <>
  <Navbar />
  <div className="container">
    
    <AlertMessage
      show={alert.show}
      type={alert.type}
      message={alert.message}
      onClose={closeAlert}
    />
    <div className="row justify-content-center align-items-center login-wrapper">

      <div className="col-md-6">

        <div className="card shadow-lg login-card">

          <div className="login-header">

            <h4 className="mb-0 fw-bold">
              Employee Management System
            </h4>

          </div>

          <div className="card-body p-4">

            <form onSubmit={handleLogin}>

              <div className="mb-3 text-start">

                <label className="form-label">
                  Username
                </label>

                <input
                  type="text"
                  className="form-control"
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />

              </div>

              <div className="mb-4 text-start">

                <label className="form-label">
                  Password
                </label>

                <input
                  type="password"
                  className="form-control"
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />

              </div>

              <div className="d-grid mb-4">

                <button
                  type="submit"
                  className="btn btn-primary login-btn"
                >
                  Login
                </button>

              </div>

              <div className="text-center">

                <a
                  href="/"
                  className="text-decoration-none login-back-link"
                >
                  ← Back to Home
                </a>

              </div>

            </form>

          </div>

        </div>

      </div>

    </div>

  </div>
  </>
  );
}

export default Login;