import { useState, useCallback } from "react";

const useFetchRequest = (showAlert) => {
  const [fetching, setFetching] = useState(false);

  const execute = useCallback(
    async (callback, errorMessage) => {
      try {
        setFetching(true);

        return await callback();
      } catch (error) {
        console.error(error);

        showAlert("danger", errorMessage);

        return null;
      } finally {
        setFetching(false);
      }
    },
    [showAlert]
  );

  return {
    fetching,
    execute,
  };
};

export default useFetchRequest;