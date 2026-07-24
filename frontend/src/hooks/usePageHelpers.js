import { useEffect } from "react";

import useAlert from "./useAlert";
import useErrorHandler from "./useErrorHandler";

import { mergeEmployeeDetails } from "../utils/mergeEmployeeDetails";

const usePageHelpers = (location = null) => {
  const {
    alert,
    showAlert,
    closeAlert,
  } = useAlert();

  const handleError = useErrorHandler(showAlert);

  useEffect(() => {
    if (!location) return;

    if (location.state?.alert) {
      showAlert(
        location.state.alert.type,
        location.state.alert.message
      );

      window.history.replaceState(
        {},
        document.title
      );
    }
  }, [location, showAlert]);

  const mergeEmployees = (
    records,
    employees,
    employeeKey = "employee"
  ) => {
    return mergeEmployeeDetails(
      records,
      employees,
      employeeKey
    );
  };

  return {
    alert,
    showAlert,
    closeAlert,

    handleError,

    mergeEmployees,
  };
};

export default usePageHelpers;