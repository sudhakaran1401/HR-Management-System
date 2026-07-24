import { useEffect } from "react";
import { useParams, useLocation } from "react-router-dom";
import Loader from "../../components/Loader";
import FormLayout from "../../layouts/FormLayout";
import FormActions from "../../components/form/FormActions";
import { InputField, SelectField, TextAreaField, ReadOnlyField, } from "../../components/form/FormElements";
import { createAttendance } from "../../services/AttendanceService";
import { getEmployee } from "../../services/EmployeeService";
import useCrudPage from "../../hooks/Crud/useCrudPage";
import useFormState from "../../hooks/useFormState";
import useEmployee, { useEmployees, } from "../../hooks/Employee/useEmployee";

const AttendanceForm = () => {
  const { id } = useParams();
  const location = useLocation();

  const {
    formData,
    handleChange,
    updateField,
  } = useFormState({
    date: new Date().toISOString().split("T")[0],
    status: "Present",
    check_in: "",
    check_out: "",
    notes: "",
    employee: "",
  });

  const {
    alert,
    closeAlert,

    fetching,
    execute,

    loading,

    handleSubmit,
  } = useCrudPage({
    createFn: createAttendance,
    updateFn: null,

    redirectPath:
      location.pathname === "/me/mark-attendance"
        ? "/me/attendance"
        : "/attendance",

    successCreate:
      "Attendance marked successfully.",

    errorMessage:
      "Failed to mark attendance.",

    buildPayload: () => ({
      employee: formData.employee,
      date: formData.date,
      status: formData.status,
      check_in: formData.check_in
        ? `${formData.check_in}:00`
        : null,
      check_out: formData.check_out
        ? `${formData.check_out}:00`
        : null,
      notes: formData.notes,
    }),
  });

  const {
    employees,
    loadEmployees,
  } = useEmployees(execute);

  const {
    employee,
    setEmployee,
    loadCurrentEmployee,
  } = useEmployee(execute);

  const fetchEmployee = async (employeeId) => {
    const employee = await execute(
      () => getEmployee(employeeId),
      "Unable to load employee details."
    );

    if (!employee) return;

    setEmployee(employee);
    updateField("employee", employee.id);
  };

  useEffect(() => {
    const load = async () => {
      if (id) {
        await fetchEmployee(id);
      } else if (
        location.pathname === "/me/mark-attendance"
      ) {
        const employee =
          await loadCurrentEmployee();

        if (employee) {
          updateField(
            "employee",
            employee.id
          );
        }
      } else if (
        location.pathname ===
        "/employees/mark-attendance"
      ) {
        await loadEmployees();

        setEmployee(null);

        updateField("employee", "");
      }
    };

    load();
  }, [id, location.pathname]);

  if (fetching && !employee) {
    return (
      <Loader title="Loading Employee..." />
    );
  }

  return (
    <FormLayout
      title="Mark Attendance"
      alert={alert}
      onClose={closeAlert}
    >
      <form onSubmit={handleSubmit}>
                {location.pathname ===
        "/employees/mark-attendance" ? (
          <SelectField
            label="Employee"
            name="employee"
            value={formData.employee}
            onChange={handleChange}
          >
            <option value="">
              Select Employee
            </option>

            {employees.map((emp) => (
              <option
                key={emp.id}
                value={emp.id}
              >
                {emp.name}
              </option>
            ))}
          </SelectField>
        ) : (
          <ReadOnlyField
            label="Employee"
            value={employee?.name || ""}
          />
        )}

        <InputField
          label="Date"
          type="date"
          className="form-control form-control-lg"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
        />

        <SelectField
          label="Status"
          className="form-select form-control-lg"
          name="status"
          value={formData.status}
          onChange={handleChange}
          required
        >
          <option value="Present">
            Present
          </option>

          <option value="Leave">
            Leave
          </option>

          <option value="Half Day">
            Half Day
          </option>

        </SelectField>
                <InputField
          label="Check In"
          type="time"
          className="form-control form-control-lg"
          name="check_in"
          value={formData.check_in}
          onChange={handleChange}
        />

        <InputField
          label="Check Out"
          type="time"
          className="form-control form-control-lg"
          name="check_out"
          value={formData.check_out}
          onChange={handleChange}
        />

        <TextAreaField
          label="Notes"
          rows={4}
          name="notes"
          value={formData.notes}
          onChange={handleChange}
          placeholder="Enter notes (optional)"
        />

        <FormActions align="center">
          <button
            type="submit"
            className="btn btn-primary px-4"
            disabled={loading}
          >
            {loading ? "Saving..." : "Save"}
          </button>
        </FormActions>

      </form>
    </FormLayout>
  );
};

export default AttendanceForm;