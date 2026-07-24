export const filterReportData = ({
  records,
  dateField,
  month = "",
  year = "",
  employee = "",
  employeeField = "employee",
}) => {
  return records.filter((record) => {
    // Employee filter
    if (
      employee !== "" &&
      Number(record[employeeField]) !== Number(employee)
    ) {
      return false;
    }

    const value = record[dateField];

    if (!value) {
      return false;
    }

    const date = new Date(value);

    if (
      month !== "" &&
      date.getMonth() + 1 !== Number(month)
    ) {
      return false;
    }

    if (
      year !== "" &&
      date.getFullYear() !== Number(year)
    ) {
      return false;
    }

    return true;
  });
};