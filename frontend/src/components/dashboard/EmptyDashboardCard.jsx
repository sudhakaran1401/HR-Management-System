const EmptyDashboardCard = ({
  message = "Use the filters above to view dashboard data.",
  fullHeight = false,
}) => {
  return (
    <div className={`card shadow-sm ${fullHeight ? "h-100" : ""}`}>
      <div
        className={`card-body d-flex justify-content-center align-items-center ${
          fullHeight ? "" : "p-5"
        }`}
      >
        <h5 className="text-muted mb-0 text-center">
          {message}
        </h5>
      </div>
    </div>
  );
};

export default EmptyDashboardCard;