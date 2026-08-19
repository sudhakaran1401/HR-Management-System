const LayoutHeader = ({
  title,
  actions = null,
  heading: Heading = "h4",
  className = "layout-header px-4 py-3 mb-3",
}) => (
  <div className={`${className} d-flex justify-content-between align-items-center`}>
    <Heading className="fw-bold mb-0">
      {title}
    </Heading>

    {actions}
  </div>
);

export default LayoutHeader;