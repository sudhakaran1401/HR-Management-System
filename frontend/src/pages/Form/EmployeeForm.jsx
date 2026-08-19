import { useEffect, useMemo, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Loader from "../../components/Loader";
import FormLayout from "../../layouts/FormLayout";
import FormActions from "../../components/form/FormActions";
import { InputField, SelectField, TextAreaField, } from "../../components/form/FormElements";
import { createEmployee, getEmployee, updateEmployee, } from "../../services/EmployeeService";
import { departments, designations, } from "../../config/constants/departments";
import useCrudPage from "../../hooks/Crud/useCrudPage";
import useFormState from "../../hooks/useFormState";

const INITIAL_FORM = {
  name: "",
  email: "",
  phone: "",
  department: "",
  designation: "",
  dob: "",
  address: "",
  photo: null,
  salary: "",
  joining_date: "",
};

const EmployeeForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();

  const isEdit = Boolean(id);

  const fileInputRef = useRef(null);

  const {
    formData,
    setFormData,
    handleChange,
  } = useFormState(INITIAL_FORM);

  const {
    alert,
    closeAlert,

    fetching,
    execute,

    loading,

    handleSubmit,
  } = useCrudPage({
    id,

    createFn: createEmployee,
    updateFn: updateEmployee,

    redirectPath: "/employees",

    successCreate:
      "Employee created successfully.",

    successUpdate:
      "Employee updated successfully.",

    errorMessage:
      "Failed to save employee.",

    buildPayload: () => {
      const data = new FormData();

      Object.entries(formData).forEach(([key, value]) => {
        if (value !== "" && value !== null) {
          data.append(key, value);
        }
      });

      return data;
    },
  });

  const inputFields = useMemo(
    () => [
      {
        label: "Name",
        name: "name",
        type: "text",
        required: true,
      },
      {
        label: "Email",
        name: "email",
        type: "email",
        required: true,
      },
      {
        label: "Phone",
        name: "phone",
        type: "text",
        required: true,
      },
      {
        label: "Date of Birth",
        name: "dob",
        type: "date",
      },
      {
        label: "Salary",
        name: "salary",
        type: "number",
      },
      {
        label: "Joining Date",
        name: "joining_date",
        type: "date",
        required: true,
      },
    ],
    []
  );

  const fetchEmployee = async () => {
    const employee = await execute(
      () => getEmployee(id),
      "Unable to load employee."
    );

    if (!employee) return;

    setFormData({
      name: employee.name || "",
      email: employee.email || "",
      phone: employee.phone || "",
      department: employee.department || "",
      designation: employee.designation || "",
      dob: employee.dob || "",
      address: employee.address || "",
      photo: null,
      salary: employee.salary || "",
      joining_date: employee.joining_date || "",
    });
  };

  useEffect(() => {
    if (isEdit) {
      fetchEmployee();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isEdit]);

  if (fetching || loading) {
    return (
      <Loader
        title={
          isEdit
            ? "Loading Employee..."
            : "Saving Employee..."
        }
      />
    );
  }

  return (
    <FormLayout
      title={isEdit ? "Edit Employee" : "Add Employee"}
      alert={alert}
      onClose={closeAlert}
      containerClass="container py-4"
      cardClass="card shadow-sm border-0"
    >
      <form onSubmit={handleSubmit}>
        <div className="row g-4">

          {inputFields.map((field) => (
            <div
              className="col-md-6"
              key={field.name}
            >
              <InputField
                label={field.label}
                type={field.type}
                name={field.name}
                value={formData[field.name] || ""}
                onChange={handleChange}
                required={field.required}
              />
            </div>
          ))}
                    <div className="col-md-6">
            <SelectField
              label="Department"
              name="department"
              value={formData.department}
              onChange={handleChange}
              options={departments}
            />
          </div>

          <div className="col-md-6">
            <SelectField
              label="Designation"
              name="designation"
              value={formData.designation}
              onChange={handleChange}
              options={designations}
            />
          </div>

          <div className="col-12">
            <TextAreaField
              label="Address"
              name="address"
              rows={3}
              value={formData.address}
              onChange={handleChange}
            />
          </div>

          <div className="col-md-6">
            <label className="form-label fw-semibold">
              Photo
            </label>

            <input
              ref={fileInputRef}
              type="file"
              className="form-control"
              name="photo"
              accept="image/*"
              onChange={handleChange}
            />

            {formData.photo && (
              <button
                type="button"
                className="btn btn-outline-danger btn-sm mt-2"
                onClick={() => {
                  setFormData((prev) => ({
                    ...prev,
                    photo: null,
                  }));

                  if (fileInputRef.current) {
                    fileInputRef.current.value = "";
                  }
                }}
              >
                Clear Image
              </button>
            )}
          </div>

        </div>

        <FormActions>

          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={() => navigate("/employees")}
          >
            Cancel
          </button>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading
              ? "Saving..."
              : isEdit
              ? "Update"
              : "Add"}
          </button>

        </FormActions>

      </form>
    </FormLayout>
  );
};

export default EmployeeForm;