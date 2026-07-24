export const mergeEmployeeDetails = (
  records,
  employees,
  employeeKey = "employee"
) => {
  const employeeMap = employees.reduce((map, emp) => {
    map[emp.id] = emp;
    return map;
  }, {});

  return records.map((record) => ({
    ...record,
    employeeDetails: employeeMap[record[employeeKey]] || null,
  }));
};