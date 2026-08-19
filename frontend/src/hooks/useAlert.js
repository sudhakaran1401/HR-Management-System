import { useCallback, useState } from "react";

const useAlert = () => {
  const [alert, setAlert] = useState({
    show: false,
    type: "",
    message: "",
  });

  const showAlert = useCallback((type, message) => {
    setAlert({
      show: true,
      type,
      message,
    });
  }, []);

  const closeAlert = useCallback(() => {
    setAlert({
      show: false,
      type: "",
      message: "",
    });
  }, []);

  return {
    alert,
    showAlert,
    closeAlert,
  };
};

export default useAlert;