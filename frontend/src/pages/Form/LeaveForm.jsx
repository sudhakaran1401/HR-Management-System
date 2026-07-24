import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Loader from "../../components/Loader";
import FormLayout from "../../layouts/FormLayout";
import FormActions from "../../components/form/FormActions";

import {
  InputField,
  SelectField,
  TextAreaField,
  ReadOnlyField,
} from "../../components/form/FormElements";

import {
  createLeave,
  updateLeave,
  getLeave,
} from "../../services/LeaveRequestService";

import useCrudPage from "../../hooks/Crud/useCrudPage";
import useEmployee, {
  useEmployees,
} from "../../hooks/Employee/useEmployee";
import useFormState from "../../hooks/useFormState";

const leaveTypeOptions = [
  {
    value: "CASUAL",
    label: "Casual Leave",
  },
  {
    value: "SICK",
    label: "Sick Leave",
  },
  {
    value: "ANNUAL",
    label: "Annual Leave",
  },
];

const LeaveForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();

  const isEdit = Boolean(id);

  const {
    formData,
    setFormData,
    handleChange,
    updateField,
  } = useFormState({
    employee: "",
    leave_type: "CASUAL",
    start_date: "",
    end_date: "",
    reason: "",
  });

  const {
    alert,
    closeAlert,
    fetching,
    execute,
    loading,
    handleSubmit,
  } = useCrudPage({
    id,
    createFn: createLeave,
    updateFn: updateLeave,
    redirectPath: "/me/leaverequests",
    successCreate: "Leave applied successfully.",
    successUpdate: "Leave updated successfully.",
    errorMessage: "Failed to save leave.",
    buildPayload: () => ({
      employee: formData.employee,
      leave_type: formData.leave_type,
      start_date: formData.start_date,
      end_date: formData.end_date,
      reason: formData.reason,
    }),
  });

  const {
    employee,
    loadCurrentEmployee,
  } = useEmployee(execute);

  const fetchLeave = async () => {
    const leave = await execute(
      () => getLeave(id),
      "Unable to load leave."
    );

    if (!leave) return;

    setFormData({
      employee: leave.employee,
      leave_type: leave.leave_type,
      start_date: leave.start_date,
      end_date: leave.end_date,
      reason: leave.reason || "",
    });
  };

  useEffect(() => {
    const load = async () => {
      const employee =
        await loadCurrentEmployee();

      if (employee) {
        updateField("employee", employee.id);
      }

      if (isEdit) {
        await fetchLeave();
      }
    };

    load();
  }, [id, isEdit]);

  if (fetching && !employee) {
    return (
      <Loader title="Loading Employee..." />
    );
  }

  return (
    <FormLayout
      title={
        isEdit
          ? "Update Leave"
          : "Apply Leave"
      }
      alert={alert}
      onClose={closeAlert}
    >
      <form onSubmit={handleSubmit}>
        <ReadOnlyField
          label="Employee"
          value={employee?.name || ""}
        />

        <SelectField
          label="Leave Type"
          name="leave_type"
          value={formData.leave_type}
          onChange={handleChange}
          options={leaveTypeOptions}
          required
          className="form-select form-control-lg"
        />

        <InputField
          label="Start Date"
          type="date"
          name="start_date"
          value={formData.start_date}
          onChange={handleChange}
          required
          className="form-control form-control-lg"
        />

        <InputField
          label="End Date"
          type="date"
          name="end_date"
          value={formData.end_date}
          onChange={handleChange}
          required
          className="form-control form-control-lg"
        />

        <TextAreaField
          label="Reason"
          rows={4}
          name="reason"
          value={formData.reason}
          onChange={handleChange}
          placeholder="Enter reason"
          required
        />
                <FormActions align="between">
          <button
            type="button"
            className="btn btn-outline-secondary btn-sm"
            onClick={() =>
              navigate("/me/leaverequests")
            }
          >
            <h6>My Requests</h6>
          </button>

          <button
            type="submit"
            className="btn btn-primary btn-sm"
            disabled={loading}
          >
            {loading
              ? "Saving..."
              : isEdit
              ? "Update"
              : "Submit"}
          </button>
        </FormActions>
      </form>
    </FormLayout>
  );
};

export default LeaveForm;