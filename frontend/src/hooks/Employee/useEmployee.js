import { useState, useCallback } from "react";
import { getCurrentEmployee, getEmployees } from "../../services/EmployeeService";


const useEmployee = (execute) => {
  const [employee, setEmployee] = useState(null);

  const loggedEmployee = JSON.parse(
    localStorage.getItem("employee")
  );

  const loadCurrentEmployee = useCallback(async () => {
    if (!execute) return null;

    const data = await execute(
      () => getCurrentEmployee(),
      "Unable to load employee details."
    );

    if (!data) return null;

    setEmployee(data);

    return data;
  }, [execute]);

  return {
    employee,
    loggedEmployee,

    setEmployee,

    loadCurrentEmployee,
  };
};

const useEmployees = (execute) => {
  const [employees, setEmployees] = useState([]);

  const loadEmployees = useCallback(async () => {
    if (!execute) return [];

    const data = await execute(
      () => getEmployees(),
      "Unable to load employees."
    );

    if (!data) return [];

    setEmployees(data);
    return data;
  }, [execute]);

  return {
    employees,
    setEmployees,
    loadEmployees,
  };
};


export { useEmployees };
export default useEmployee;