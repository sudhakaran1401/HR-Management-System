import { useState } from "react";

const useReportFilters = (showEmployee = true) => {
  const [month, setMonth] = useState("");
  const [year, setYear] = useState("");

  const [employee, setEmployee] = useState("");

  const [appliedMonth, setAppliedMonth] = useState("");
  const [appliedYear, setAppliedYear] = useState("");

  const [appliedEmployee, setAppliedEmployee] = useState("");

  const [reportGenerated, setReportGenerated] = useState(false);

  const handleGenerate = () => {
    setAppliedMonth(month);
    setAppliedYear(year);

    if (showEmployee) {
      setAppliedEmployee(employee);
    }

    setReportGenerated(true);
  };

  const handleReset = () => {
    setMonth("");
    setYear("");
    setEmployee("");

    setAppliedMonth("");
    setAppliedYear("");
    setAppliedEmployee("");

    setReportGenerated(false);
  };

  return {
    month,
    year,
    employee,

    appliedMonth,
    appliedYear,
    appliedEmployee,

    reportGenerated,

    setMonth,
    setYear,
    setEmployee,

    handleGenerate,
    handleReset,
  };
};

export default useReportFilters;