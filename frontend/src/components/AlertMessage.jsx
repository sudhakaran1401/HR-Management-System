import { useEffect } from "react";

function AlertMessage({
  show,
  type,
  message,
  onClose,
  duration = 3000,
}) {
  useEffect(() => {
    if (!show) return;

    const timer = setTimeout(() => {
      onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [show, duration, onClose]);

  if (!show) return null;

  return (
    <div
      className={`container alert alert-${type} alert-dismissible fade show`} 
      role="alert"
    >
      {message}

      <button
        type="button"
        className="btn-close"
        onClick={onClose}
      />
    </div>
  );
}

export default AlertMessage;