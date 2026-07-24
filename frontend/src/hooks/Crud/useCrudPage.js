import useAlert from "../useAlert";
import useFetchRequest from "../useFetchRequest";
import useCrudForm from "./useCrudForm";
import useSubmitHandler from "../useSubmitHandler";

const useCrudPage = ({
  id = null,

  createFn,
  updateFn,

  redirectPath,

  successCreate,
  successUpdate,

  errorMessage,

  buildPayload,
}) => {
  const {
    alert,
    showAlert,
    closeAlert,
  } = useAlert();

  const {
    fetching,
    execute,
  } = useFetchRequest(showAlert);

  const {
    loading,
    submit,
  } = useCrudForm({
    id,
    createFn,
    updateFn,
    redirectPath,
    successCreate,
    successUpdate,
  });

  const handleSubmit = useSubmitHandler({
    submit,
    showAlert,
    errorMessage,
    buildPayload,
  });

  return {
    alert,
    showAlert,
    closeAlert,

    fetching,
    execute,

    loading,

    handleSubmit,
  };
};

export default useCrudPage;