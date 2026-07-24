import { useEffect, useMemo } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Loader from "../../components/Loader";
import FormLayout from "../../layouts/FormLayout";
import FormActions from "../../components/form/FormActions";
import { InputField, SelectField, TextAreaField, ReadOnlyField, } from "../../components/form/FormElements";
import { createPayroll, updatePayroll, getPayrollById, } from "../../services/PayrollService";
import useCrudPage from "../../hooks/Crud/useCrudPage";
import useFormState from "../../hooks/useFormState";
import useEmployee, { useEmployees, } from "../../hooks/Employee/useEmployee";

const PayrollForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();

  const {
    formData,
    setFormData,
    handleChange,
    updateFields,
  } = useFormState({
    employee: "",
    pay_month: "",
    amt_per_day: "",
    basic: "",
    hra: "",
    allowances: "",
    pf: "",
    tax: "",
    other_deductions: "",
    paid_date: "",
    notes: "",
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

    createFn: createPayroll,
    updateFn: updatePayroll,

    redirectPath: "/payroll",

    successCreate:
      "Payroll created successfully.",

    successUpdate:
      "Payroll updated successfully.",

    errorMessage:
      "Something went wrong.",

    buildPayload: () => formData,
  });

  const {
    employees,
    loadEmployees,
  } = useEmployees(execute);

  const earningsFields = useMemo(
    () => [
      {
        label: "Basic",
        field: "basic",
      },
      {
        label: "HRA",
        field: "hra",
      },
      {
        label: "Allowances",
        field: "allowances",
      },
    ],
    []
  );

  const deductionFields = useMemo(
    () => [
      {
        label: "PF",
        field: "pf",
      },
      {
        label: "Tax",
        field: "tax",
      },
      {
        label: "Other Deductions",
        field: "other_deductions",
      },
    ],
    []
  );

  const fetchPayroll = async () => {
    if (!id) return;

    const payroll = await execute(
      () => getPayrollById(id),
      "Unable to load payroll."
    );

    if (!payroll) return;

    setFormData(payroll);
  };

  useEffect(() => {
    loadEmployees();

    if (id) {
      fetchPayroll();
    }

    // eslint-disable-next-line
  }, [id]);

  useEffect(() => {
    const amt = parseFloat(
      formData.amt_per_day
    );

    if (!amt) {
      updateFields({
        basic: "",
        hra: "",
        allowances: "",
        pf: "",
        tax: "",
        other_deductions: "",
      });

      return;
    }

    const monthly = amt * 30;

    updateFields({
      basic: (monthly * 0.70).toFixed(2),
      hra: (monthly * 0.20).toFixed(2),
      allowances: (monthly * 0.10).toFixed(2),
      pf: (monthly * 0.70 * 0.05).toFixed(2),
      tax: (monthly * 0.70 * 0.02).toFixed(2),
      other_deductions: "0.00",
    });
  }, [formData.amt_per_day, updateFields]);

  if (fetching) {
    return (
      <Loader title="Loading Payroll..." />
    );
  }

  return (
    <FormLayout
      title={
        id
          ? "Update Payroll"
          : "Add Payroll"
      }
      alert={alert}
      onClose={closeAlert}
      backPath="/payroll"
      containerClass="container-fluid py-4 form-container-sm"
      cardClass="card shadow-sm border-0 mx-auto form-card-lg"
    >
          <form onSubmit={handleSubmit}>

        <div className="row g-3 mb-3">

          <div className="col-md-6">
            <SelectField
              label="Employee"
              name="employee"
              value={formData.employee}
              onChange={handleChange}
              required
              placeholder="Select Employee"
              options={employees.map((emp) => ({
                value: emp.id,
                label: emp.name,
              }))}
            />
          </div>

          <div className="col-md-6">
            <InputField
              label="Pay Month"
              type="date"
              name="pay_month"
              value={formData.pay_month}
              onChange={handleChange}
              required
            />
          </div>

        </div>

        <hr className="my-4" />

        <h5 className="fw-bold mb-3">
          Earnings
        </h5>

        <div className="row g-3">

          <div className="col-md-4">
            <InputField
              label="Amount / Day"
              type="number"
              name="amt_per_day"
              value={formData.amt_per_day}
              onChange={handleChange}
              required
            />
          </div>

          {earningsFields.map((field) => (
            <div
              className="col-md-4"
              key={field.field}
            >
              <ReadOnlyField
                label={field.label}
                value={formData[field.field]}
              />
            </div>
          ))}

        </div>

        <hr className="my-4" />

        <h5 className="fw-bold mb-3">
          Deductions
        </h5>

        <div className="row g-3">

          {deductionFields.map((field) => (
            <div
              className="col-md-4"
              key={field.field}
            >
              <ReadOnlyField
                label={field.label}
                value={formData[field.field]}
              />
            </div>
          ))}

          <div className="col-md-6">
            <InputField
              label="Paid Date"
              type="date"
              name="paid_date"
              value={formData.paid_date}
              onChange={handleChange}
            />
          </div>

        </div>

        <div className="mt-4">
          <TextAreaField
            label="Notes"
            rows={4}
            name="notes"
            value={formData.notes}
            onChange={handleChange}
          />
        </div>
                <FormActions>

          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={() => navigate("/payroll")}
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
              : id
              ? "Update Payroll"
              : "Create Payroll"}
          </button>

        </FormActions>

      </form>
    </FormLayout>
  );
};

export default PayrollForm;