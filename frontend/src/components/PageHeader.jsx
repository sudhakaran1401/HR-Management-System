import { useNavigate } from "react-router-dom";

const PageHeader = ({
  title,
  showBack = true,
  backPath = null,
  actions,
  className = "",
}) => {
  const navigate = useNavigate();

  const handleBack = () => {
    if (backPath) {
      navigate(backPath);
    } else {
      navigate(-1);
    }
  };

  return (
    <div
      className={`page-header d-flex justify-content-between align-items-center px-4 py-3 mb-4 ${className}`}
    >
      <h4 className="page-title mb-0 fw-bold">
        {title}
      </h4>

      <div className="d-flex gap-2">
        {actions}

        {showBack && (
          <button
            type="button"
            className="btn btn-light"
            onClick={handleBack}
          >
            Back
          </button>
        )}
      </div>
    </div>
  );
};

export default PageHeader;