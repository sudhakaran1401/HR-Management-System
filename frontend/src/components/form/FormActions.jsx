const FormActions = ({
  align = "end",
  children,
}) => {
  const justify =
    align === "between"
      ? "justify-content-between"
      : align === "center"
      ? "justify-content-center"
      : "justify-content-end";

  return (
    <div className={`d-flex ${justify} gap-3 mt-4`}>
      {children}
    </div>
  );
};

export default FormActions;