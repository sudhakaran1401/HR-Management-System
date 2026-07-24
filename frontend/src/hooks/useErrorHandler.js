import { useCallback } from "react";

const useErrorHandler = (showAlert) => {
  return useCallback(
    (error, defaultMessage = "Something went wrong.") => {
      console.error(error);

      showAlert(
        "danger",
        error?.response?.data?.error || defaultMessage
      );
    },
    [showAlert]
  );
};

export default useErrorHandler;