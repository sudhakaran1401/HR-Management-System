function ViewButton({
  text = "View",
  onClick,
  className = "btn btn-outline-primary btn-sm w-100 mt-2",
}) {
  return (
    <button
      type="button"
      className={className}
      onClick={onClick}
    >
      {text}
    </button>
  );
}

export default ViewButton;