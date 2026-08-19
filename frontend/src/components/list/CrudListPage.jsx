import { useLocation, useNavigate } from "react-router-dom";

import AlertMessage from "../AlertMessage";
import ModuleLayout from "../../layouts/ModuleLayout";

import useListPage from "../../hooks/useListPage";
import usePageHelpers from "../../hooks/usePageHelpers";

const CrudListPage = ({
  title,

  buttonText = null,
  onButtonClick,

  searchPlaceholder = "Search...",

  columns,

  loadData,

  filterData,

  transformData,

  dependencies = [],

  errorMessage = "Unable to load records.",
}) => {

  const navigate = useNavigate();
  const location = useLocation();

  const {
    alert,
    showAlert,
    closeAlert,
    handleError,
    mergeEmployees,
  } = usePageHelpers(location);

  const {
    loading,
    search,
    setSearch,
    table,
    reload,
  } = useListPage({

    dependencies,

    loadData: () =>
      loadData({
        navigate,
        location,
        mergeEmployees,
        reload,
        showAlert,
        handleError,
      }),

    filterData: filterData
      ? (records) =>
          filterData(records, {
            navigate,
            location,
            mergeEmployees,
            reload,
            showAlert,
            handleError,
          })
      : undefined,

    transformData: transformData
      ? (records) =>
          transformData(records, {
            navigate,
            location,
            mergeEmployees,
            reload,
            showAlert,
            handleError,
          })
      : undefined,

    onError: (error) =>
      handleError(
        error,
        errorMessage
      ),
  });

  const context = {
  navigate,
  location,
  mergeEmployees,
  reload,
  showAlert,
  handleError,
};

  const resolvedColumns =
    typeof columns === "function"
      ? columns(context)
      : columns;

  const resolvedButtonText =
    typeof buttonText === "function"
      ? buttonText(context)
      : buttonText;

  return (
    <>
      <AlertMessage
        show={alert.show}
        type={alert.type}
        message={alert.message}
        onClose={closeAlert}
      />

      <ModuleLayout
        title={title}
        buttonText={resolvedButtonText}
        onButtonClick={
          onButtonClick
            ? () =>
                onButtonClick({
                  navigate,
                  location,
                  mergeEmployees,
                  reload,
                  showAlert,
                  handleError,
                })
            : undefined
        }
        searchPlaceholder={searchPlaceholder}
        search={search}
        onSearch={setSearch}
        columns={resolvedColumns}
        data={table.paginatedData}
        loading={loading}
        table={table}
      />
    </>
  );
};

export default CrudListPage;