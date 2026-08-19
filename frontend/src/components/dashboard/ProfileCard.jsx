import { useNavigate } from "react-router-dom";

const ProfileCard = ({ profile }) => {
  const navigate = useNavigate();

  return (
    <div className="card shadow-sm h-100">
      <div className="card-body">
        <h5 className="fw-bold mb-4">
          My Profile
        </h5>

        <p>
          <strong>Name:</strong>{" "}
          {profile?.name || "N/A"}
        </p>

        <p>
          <strong>Email:</strong>{" "}
          {profile?.email || "N/A"}
        </p>

        <p>
          <strong>Department:</strong>{" "}
          {profile?.department || "N/A"}
        </p>

        <p>
          <strong>Designation:</strong>{" "}
          {profile?.designation || "N/A"}
        </p>

        <div className="mt-4">
          <button
            className="btn btn-outline-secondary w-30"
            onClick={() => navigate("/me/profile")}
          >
            View Profile
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfileCard;