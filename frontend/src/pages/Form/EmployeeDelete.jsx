import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getEmployee, deleteEmployee } from "../../services/EmployeeService";
import AlertMessage from "../../components/AlertMessage";
import useAlert from "../../hooks/useAlert";
import Loader from "../../components/Loader";

const DeleteEmployee = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { alert, showAlert, closeAlert } = useAlert();
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    fetchEmployee();
  }, []);

  const fetchEmployee = async () => {
    try {
      const data = await getEmployee(id);
      setEmployee(data);
    } catch (error) {
      console.error("Error fetching employee:", error);
      navigate("/employees", {
      state: {
        alert: {
          type: "danger",
          message: "Unable to load employee details.",
        },
      },
    });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
  try {
    setDeleting(true);

    await deleteEmployee(id);

    navigate("/employees", {
      state: {
        alert: {
          type: "success",
          message: "Employee deleted successfully.",
        },
      },
    });
  } catch (error) {
    console.error("Delete Error:", error);
    // Show your custom error toast/modal here if you have one
  } finally {
    setDeleting(false);
  }
};

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <h4>Loading...</h4>
      </div>
    );
  }

  return (

  <>
  <AlertMessage
    show={alert.show}
    type={alert.type}
    message={alert.message}
    onClose={closeAlert}
  />
  <div className="container vh-90 mt-5">

    <div className="card shadow mx-auto delete-card">

      <div className="card-header text-white delete-header">

        <h4 className="mb-0">
          Confirm Deletion
        </h4>

      </div>

      <div className="card-body text-center p-4">

        <p className="fs-5">
          Are you sure you want to delete
        </p>

        <h3 className="text-danger fw-bold mb-4">
          {employee?.name} ?
        </h3>

        <div className="d-flex justify-content-center gap-3">

          <button
            className="btn btn-danger"
            onClick={handleDelete}
            disabled={deleting}
          >
            {deleting ? "Deleting..." : "Yes, Delete"}
          </button>

          <button
            className="btn btn-secondary"
            onClick={() => navigate(-1)}
            disabled={deleting}
          >
            Cancel
          </button>

        </div>

      </div>

    </div>

  </div>
  </>
  );
};

export default DeleteEmployee;