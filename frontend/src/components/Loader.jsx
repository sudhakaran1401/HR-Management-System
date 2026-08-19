const Loader = ({ title = "Loading..." }) => {
  return (
    <div className="container py-5">
      <div className="text-center">
        <div
          className="spinner-border text-primary"
          role="status"
        >
          <span className="visually-hidden">
            Loading...
          </span>
        </div>

        <h5 className="mt-3">{title}</h5>
      </div>
    </div>
  );
};

export default Loader;