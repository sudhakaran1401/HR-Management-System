import { useNavigate } from "react-router-dom";

const ReportButtons = ({ buttons = [] }) => {
  const navigate = useNavigate();

  return (
    <div className="d-flex gap-5 flex-wrap mt-5 justify-content-center">
      {buttons.map((button) => (
        <button
          key={button.path}
          className={button.className}
          onClick={() => navigate(button.path)}
        >
          {button.label}
        </button>
      ))}
    </div>
  );
};

export default ReportButtons;