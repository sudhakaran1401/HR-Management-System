// hooks/useSubmitHandler.js

const useSubmitHandler = ({
  submit,
  showAlert,
  errorMessage,
  buildPayload,
}) => {
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const payload = buildPayload();

      await submit(payload);

    } catch (error) {
      console.error(error);

      showAlert(
        "danger",
        error.response?.data?.error ||
          errorMessage
      );
    }
  };

  return handleSubmit;
};

export default useSubmitHandler;