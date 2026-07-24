import { useState } from "react";

const Avatar = ({ src }) => {
  const [hasError, setHasError] = useState(false);

  if (!src || hasError) {
    return <span>-</span>;
  }

  return (
    <img
      src={src}
      alt="Profile"
      className="avatar"
      onError={() => setHasError(true)}
    />
  );
};

export default Avatar;