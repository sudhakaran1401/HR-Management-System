import Avatar from "../../components/Avatar";
import ActionButtons from "../../components/ActionButtons";
import { formatDate } from "../../utils/formatters";

export const employeeColumns = (
  showActions = true,
  navigate
) => {
  const columns = [
    {
      key: "photo",
      title: "",
      width: "70px",
      render: (row) => (
        <Avatar
          src={row.photo}
          alt={row.name}
        />
      ),
    },

    {
      key: "name",
      title: "Name",
      width: "280px",
    },

    {
      key: "email",
      title: "Email",
      width: "220px",
    },

    {
      key: "phone",
      title: "Phone",
      width: "150px",
    },

    {
      key: "department",
      title: "Department",
      width: "150px",
    },

    {
      key: "designation",
      title: "Designation",
      width: "300px",
    },

    {
      key: "joining_date",
      title: "Joining Date",
      width: "150px",
      render: (row) => formatDate(row.joining_date),
    },
  ];

  if (showActions) {
    columns.push({
      key: "actions",
      title: "Actions",
      width: "320px",

      render: (row) => (
        <ActionButtons>
          <button
            className="btn btn-info btn-sm"
            onClick={() =>
              navigate(`/employees/${row.id}`)
            }
          >
            View
          </button>

          <button
            className="btn btn-warning btn-sm"
            onClick={() =>
              navigate(`/employees/edit/${row.id}`)
            }
          >
            Edit
          </button>

          <button
            className="btn btn-danger btn-sm"
            onClick={() =>
              navigate(`/employees/delete/${row.id}`)
            }
          >
            Delete
          </button>

          <button
            className="btn btn-primary btn-sm"
            onClick={() =>
              navigate(
                `/employee/${row.id}/mark-attendance`
              )
            }
          >
            Attendance
          </button>
        </ActionButtons>
      ),
    });
  }

  return columns;
};