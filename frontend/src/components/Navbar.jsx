import { Link, useNavigate } from "react-router-dom";
import ThemeToggle from "./ThemeToggle";

function Navbar() {
  const navigate = useNavigate();

  const employee = JSON.parse(
    localStorage.getItem("employee")
  );

  const isHR = employee?.department === "HR";

  const dashboardMode =
    localStorage.getItem("dashboard_mode") ||
    "employee";

  // True only when HR is currently viewing the HR dashboard
  const isHRView =
    isHR && dashboardMode === "hr";

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow fixed-top">
      <div className="container-fluid">

        {/* Brand */}
        <Link
          className="navbar-brand text-white"
          to={
            isHRView
              ? "/hr/dashboard"
              : "/me/dashboard"
          }
        >
          Employee Management System
        </Link>

        {/* Mobile Toggle */}
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        {/* Right Side */}
        <div
          className="collapse navbar-collapse"
          id="navbarNav"
        >
          <ul className="navbar-nav ms-auto align-items-center gap-4">

            {/* Theme Toggle */}
            <li className="nav-item">
              <ThemeToggle />
            </li>

            {/* User Dropdown */}
            <li className="nav-item dropdown">

              <a
                href="#"
                className="nav-link dropdown-toggle text-white fw-semibold"
                id="userDropdown"
                role="button"
                data-bs-toggle="dropdown"
              >
                {employee?.username ||
                  employee?.name ||
                  "User"}
              </a>

              <ul className="dropdown-menu dropdown-menu-end dropdown-menu-dark">

                {/* Common */}
                <li>
                  <Link
                    className="dropdown-item"
                    to={
                      isHRView
                        ? "/hr/dashboard"
                        : "/me/dashboard"
                    }
                  >
                    Dashboard
                  </Link>
                </li>

                <li>
                  <Link
                    className="dropdown-item"
                    to={
                      isHRView
                        ? `/employees/${employee?.id}`
                        : "/me/profile"
                    }
                  >
                    Profile
                  </Link>
                </li>

                <li>
                  <hr className="dropdown-divider" />
                </li>

                {/* Employee Menu */}
                {!isHRView && (
                  <>
                    <li>
                      <Link
                        className="dropdown-item"
                        to="/me/leaverequests"
                      >
                        My Leaves
                      </Link>
                    </li>

                    <li>
                      <Link
                        className="dropdown-item"
                        to="/me/attendance"
                      >
                        My Attendance
                      </Link>
                    </li>

                    <li>
                      <Link
                        className="dropdown-item"
                        to="/me/payroll"
                      >
                        My Payroll
                      </Link>
                    </li>
                  </>
                )}

                {/* HR Menu */}
                {isHRView && (
                  <>
                    <li>
                      <Link
                        className="dropdown-item"
                        to="/employees/mark-attendance"
                      >
                        Mark Attendance
                      </Link>
                    </li>

                    <li>
                      <Link
                        className="dropdown-item"
                        to="/payroll/create"
                      >
                        Create Payroll
                      </Link>
                    </li>

                    <li>
                      <Link
                        className="dropdown-item"
                        to="/payroll"
                      >
                        Payroll List
                      </Link>
                    </li>
                  </>
                )}

                <li>
                  <hr className="dropdown-divider" />
                </li>

                <li>
                  <button
                    className="dropdown-item"
                    onClick={handleLogout}
                  >
                    Logout
                  </button>
                </li>

              </ul>
            </li>

          </ul>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;