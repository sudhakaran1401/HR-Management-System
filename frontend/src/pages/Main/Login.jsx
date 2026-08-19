import { useState } from "react";
import AlertMessage from "../../components/AlertMessage";
import api from "../../services/api";
import useAlert from "../../hooks/useAlert";
import Navbar from "../../components/Navbar";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();
  const { alert, showAlert, closeAlert } = useAlert();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // --------------------------------------------------
      // 1. Login
      // --------------------------------------------------
      const response = await api.post("/api/token/", {
        username,
        password,
      });

      console.log("TOKEN SUCCESS:", response.status);

      const access = response.data.access;
      const refresh = response.data.refresh;

      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);

      // --------------------------------------------------
      // 2. Get logged-in user
      // --------------------------------------------------
      const userRes = await api.get("/api/me/", {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      });

      console.log(
        "ME SUCCESS:",
        userRes.status,
        userRes.data
      );

      const userId = userRes.data.id;

      // --------------------------------------------------
      // 3. Determine HR user
      // --------------------------------------------------
      const isHR = userRes.data.is_hr === true;

      console.log("IS HR:", isHR);

      // --------------------------------------------------
      // 4. HR does not require employee profile
      // --------------------------------------------------
      if (isHR) {

        localStorage.setItem(
          "employee",
          JSON.stringify({
            id: userRes.data.id,
            username: userRes.data.username || username,
            name: userRes.data.name || username,
            department: "HR",
            designation: userRes.data.designation || "HR Manager",
          })
        );
        
        localStorage.setItem(
          "dashboard_mode",
          "hr"
        );

        sessionStorage.setItem(
          "alert",
          JSON.stringify({
            type: "success",
            message: "Login successful.",
          })
        );

        navigate("/hr/dashboard");
        return;
      }

      // --------------------------------------------------
      // 5. Get employee profile
      // --------------------------------------------------
      const employeeRes = await api.get(
        "/api/employees/me/",
        {
          headers: {
            Authorization: `Bearer ${access}`,
          },
        }
      );

      console.log(
        "EMPLOYEE PROFILE SUCCESS:",
        employeeRes.status
      );

      console.log(
        "EMPLOYEE PROFILE:",
        employeeRes.data
      );

      const employee = employeeRes.data;

      if (!employee) {
        console.error(
          "Employee profile not found for user:",
          userId
        );

        showAlert(
          "danger",
          "Employee profile not found."
        );

        return;
      }

      console.log("USER ID:", userId);
      console.log("MATCHED EMPLOYEE:", employee);

      // --------------------------------------------------
      // 6. Save employee details
      // --------------------------------------------------
      localStorage.setItem(
        "employee",
        JSON.stringify(employee)
      );

      localStorage.setItem(
        "dashboard_mode",
        "employee"
      );

      // --------------------------------------------------
      // 7. Success message
      // --------------------------------------------------
      sessionStorage.setItem(
        "alert",
        JSON.stringify({
          type: "success",
          message: "Login successful.",
        })
      );

      // --------------------------------------------------
      // 8. Navigate employee
      // --------------------------------------------------
      navigate("/me/dashboard");
    } catch (error) {
      console.error("=================================");
      console.error("LOGIN FAILED");
      console.error("URL:", error.config?.url);
      console.error("STATUS:", error.response?.status);
      console.error("DATA:", error.response?.data);
      console.error("MESSAGE:", error.message);
      console.error("=================================");

      showAlert(
        "danger",
        "Invalid Credentials."
      );
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
                  HR Management System
                </h4>
              </div>

              <div className="card-body p-4">
                <form onSubmit={handleLogin}>
                  <div className="mb-3 text-start">
                    <label
                      htmlFor="username"
                      className="form-label"
                    >
                      Username
                    </label>

                    <input
                      id="username"
                      type="text"
                      className="form-control"
                      placeholder="Enter username"
                      value={username}
                      onChange={(e) =>
                        setUsername(e.target.value)
                      }
                      required
                    />
                  </div>

                  <div className="mb-4 text-start">
                    <label
                      htmlFor="password"
                      className="form-label"
                    >
                      Password
                    </label>

                    <input
                      id="password"
                      type="password"
                      className="form-control"
                      placeholder="Enter password"
                      value={password}
                      onChange={(e) =>
                        setPassword(e.target.value)
                      }
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