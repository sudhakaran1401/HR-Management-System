const EmptyReport = ({
  message = "Use the filters above to generate a report.",
  padding = "py-3",
}) => {
  return (
    <div className="card shadow-sm border-0">
      <div className={`card-body text-center ${padding} text-muted`}>
        <p className="mb-0">{message}</p>
      </div>
    </div>
  );
};

export default EmptyReport;