import { useEffect, useState } from "react";
import { getEmployees } from "../../services/EmployeeService";
import { mergeEmployeeDetails } from "../../utils/mergeEmployeeDetails";

const useReportData = (service) => {
  const [data, setData] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      const [records, employeeData] = await Promise.all([
        service(),
        getEmployees(),
      ]);

      setEmployees(employeeData);

      const merged = mergeEmployeeDetails(records, employeeData);

      setData(merged);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return {
    data,
    employees,
    loading,
    reload: loadData,
  };
};

export default useReportData;