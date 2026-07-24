import { useNavigate } from "react-router-dom";
import CrudListPage from "../../components/list/CrudListPage";
import { employeeColumns } from "../../config/columns/EmployeeColumns";
import { getEmployees } from "../../services/EmployeeService";

const Employees = () => {
  const navigate = useNavigate();

  return (
    <CrudListPage
      title="Employees"
      buttonText="+ Add Employee"
      searchPlaceholder="Search employees..."
      columns={employeeColumns(true, navigate)}
      loadData={getEmployees}
      errorMessage="Unable to load employees."
      onButtonClick={() =>
        navigate("/employees/create")
      }
    />
  );
};

export default Employees;