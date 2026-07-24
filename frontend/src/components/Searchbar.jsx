import React from "react";

const SearchBar = ({
  placeholder,
  value,
  onChange,
}) => {
  return (
    <div className="my-2">
      <input
        type="text"
        className="form-control"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
};

export default SearchBar;