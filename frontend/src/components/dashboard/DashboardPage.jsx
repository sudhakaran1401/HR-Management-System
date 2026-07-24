import AlertMessage from "../AlertMessage";
import DashboardHeader from "./DashboardHeader";

const DashboardPage = ({
  title,
  alert,
  onClose,
  headerProps,
  children,
}) => {
  return (
    <div className="container mt-4">
      <AlertMessage
        show={alert.show}
        type={alert.type}
        message={alert.message}
        onClose={onClose}
      />

      <DashboardHeader
        title={title}
        {...headerProps}
      />

      {children}
    </div>
  );
};

export default DashboardPage;