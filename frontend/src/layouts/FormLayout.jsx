import AlertMessage from "../components/AlertMessage";
import PageHeader from "../components/PageHeader";

const FormLayout = ({
  title,

  alert = null,
  onClose,

  actions = null,
  backPath = null,

  containerClass = "container-fluid py-4 form-container",
  cardClass = "card shadow-sm border-0 mx-auto form-card",
  bodyClass = "card-body p-4",

  children,
}) => {
  return (
    <div className={containerClass}>

      {alert && (
        <AlertMessage
          show={alert.show}
          type={alert.type}
          message={alert.message}
          onClose={onClose}
        />
      )}

      <PageHeader
        title={title}
        actions={actions}
        backPath={backPath}
      />

      <div className={cardClass}>
        <div className={bodyClass}>
          {children}
        </div>
      </div>

    </div>
  );
};

export default FormLayout;