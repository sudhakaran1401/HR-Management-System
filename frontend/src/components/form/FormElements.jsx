import React from "react";

const Label = ({ children, required }) => (
  <label className="form-label fw-semibold">
    {children}
    {required && (
      <span className="text-danger ms-1">*</span>
    )}
  </label>
);

export const InputField = ({
  label,
  colClass,
  className = "form-control",
  required = false,
  ...props
}) => {
  const content = (
    <>
      <Label required={required}>
        {label}
      </Label>

      <input
        className={className}
        required={required}
        {...props}
      />
    </>
  );

  return colClass ? (
    <div className={colClass}>{content}</div>
  ) : (
    <div className="mb-3">{content}</div>
  );
};

export const SelectField = ({
  label,
  options = [],
  placeholder,
  colClass,
  className = "form-select",
  required = false,
  children,
  ...props
}) => {
  const content = (
    <>
      <Label required={required}>
        {label}
      </Label>

      <select
        className={className}
        required={required}
        {...props}
      >
        {placeholder && (
          <option value="">
            {placeholder}
          </option>
        )}

        {children
          ? children
          : options.map((option) => (
              <option
                key={option.value}
                value={option.value}
              >
                {option.label}
              </option>
            ))}
      </select>
    </>
  );

  return colClass ? (
    <div className={colClass}>{content}</div>
  ) : (
    <div className="mb-3">{content}</div>
  );
};

export const TextAreaField = ({
  label,
  rows = 4,
  colClass,
  className = "form-control",
  required = false,
  ...props
}) => {
  const content = (
    <>
      <Label required={required}>
        {label}
      </Label>

      <textarea
        rows={rows}
        className={className}
        required={required}
        {...props}
      />
    </>
  );

  return colClass ? (
    <div className={colClass}>{content}</div>
  ) : (
    <div className="mb-3">{content}</div>
  );
};

export const ReadOnlyField = ({
  label,
  value,
  colClass,
  className = "form-control",
}) => {
  const content = (
    <>
      <Label>{label}</Label>

      <input
        className={className}
        value={value ?? ""}
        readOnly
      />
    </>
  );

  return colClass ? (
    <div className={colClass}>{content}</div>
  ) : (
    <div className="mb-3">{content}</div>
  );
};