const useReportExport = ({
  showAlert,
  csvAction,
  pdfAction,
  moduleName,
  params,
}) => {
  const download = async ({
    action,
    successMessage,
    errorMessage,
  }) => {
    try {
      await action(params);

      showAlert(
        "success",
        successMessage
      );
    } catch (error) {
      console.error(error);

      showAlert(
        "danger",
        errorMessage
      );
    }
  };

  const handleCSV = () =>
    download({
      action: csvAction,
      successMessage: `${moduleName} CSV downloaded successfully.`,
      errorMessage: `Failed to download ${moduleName} CSV.`,
    });

  const handlePDF = () =>
    download({
      action: pdfAction,
      successMessage: `${moduleName} PDF downloaded successfully.`,
      errorMessage: `Failed to download ${moduleName} PDF.`,
    });

  return {
    handleCSV,
    handlePDF,
  };
};

export default useReportExport;