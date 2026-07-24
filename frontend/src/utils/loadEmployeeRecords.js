import { getEmployees } from "../services/EmployeeService";

const loadEmployeeRecords = async ({
  service,
  mergeEmployees = null,
  transform = null,
  employeeKey = "employee",
  returnRaw = false,
}) => {
  const [records, employees] = await Promise.all([
    service(),
    getEmployees(),
  ]);

  if (returnRaw) {
    return {
      records,
      employees,
    };
  }

  let data = mergeEmployees
    ? mergeEmployees(records, employees, employeeKey)
    : records;

  if (transform) {
    data = transform(data);
  }

  return data;
};

export default loadEmployeeRecords;