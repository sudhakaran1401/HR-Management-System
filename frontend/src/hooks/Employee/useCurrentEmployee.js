import { useState, useCallback } from "react";
import { getCurrentEmployee } from "../services/EmployeeService";

const useCurrentEmployee = (execute) => {
  const [employee, setEmployee] = useState(null);

  const loadCurrentEmployee = useCallback(async () => {
    const employee = await execute(
      () => getCurrentEmployee(),
      "Unable to load employee details."
    );

    if (!employee) return null;

    setEmployee(employee);

    return employee;
  }, [execute]);

  return {
    employee,
    setEmployee,
    loadCurrentEmployee,
  };
};

export default useCurrentEmployee;