import { getEmployees } from "../services/EmployeeService";

const loadEmployeeRecords = async ({
  service,
  mergeEmployees = null,
  transform = null,
  employeeKey = "employee",
  returnRaw = false,
  loadEmployees = true,
  employee = null,
}) => {
  
  const recordsPromise = service();

  const employeesPromise = loadEmployees
    ? getEmployees()
    : Promise.resolve(employee ? [employee] : []);

  const [records, employees] = await Promise.all([
    recordsPromise,
    employeesPromise,
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
