import { useParams } from "react-router-dom";
import CrudListPage from "../../components/list/CrudListPage";
import { leaveColumns } from "../../config/columns/LeaverequestColumns";
import { getLeaves, approveLeave, rejectLeave, } from "../../services/LeaveRequestService";
import loadEmployeeRecords from "../../utils/loadEmployeeRecords";
import useLoggedEmployee from "../../hooks/Employee/useLoggedEmployee";

const Leave = () => {
  const { employeeId } = useParams();

  const loggedEmployee = useLoggedEmployee();

  return (
    <CrudListPage
      title="Leave Requests"
      buttonText={
        location.pathname === "/me/leaverequests"
          ? "Apply Leave"
          : null
      }
      searchPlaceholder="Search leave requests..."
      dependencies={[employeeId]}
      columns={({ location }) =>
        leaveColumns({
          isHRPage:
            location.pathname !== "/me/leaverequests",

          isMyLeavePage:
            location.pathname === "/me/leaverequests",
        })
      }
      loadData={({
        mergeEmployees,
        reload,
        showAlert,
        handleError,
        navigate,
      }) =>
        loadEmployeeRecords({
          service: getLeaves,
          mergeEmployees,

          transform: (records) =>
            records.map((leave) => ({
              ...leave,

              onUpdate: (id) =>
                navigate(`/leaverequest/edit/${id}`),

              onApprove: async (id) => {
                try {
                  await approveLeave(id);

                  showAlert(
                    "success",
                    "Leave approved successfully."
                  );

                  reload();
                } catch (error) {
                  handleError(
                    error,
                    "Failed to approve leave."
                  );
                }
              },

              onReject: async (id) => {
                try {
                  await rejectLeave(id);

                  showAlert(
                    "success",
                    "Leave rejected successfully."
                  );

                  reload();
                } catch (error) {
                  handleError(
                    error,
                    "Failed to reject leave."
                  );
                }
              },
            })),
        })
      }
      filterData={(records, { location }) => {
        if (
          location.pathname ===
          "/me/leaverequests"
        ) {
          return records.filter(
            (leave) =>
              Number(leave.employee) ===
              Number(loggedEmployee?.id)
          );
        }

        if (employeeId) {
          return records.filter(
            (leave) =>
              Number(leave.employee) ===
              Number(employeeId)
          );
        }

        return records;
      }}
      onButtonClick={({ navigate }) =>
        navigate("/leaverequest/create")
      }
      errorMessage="Failed to load leave requests."
    />
  );
};

export default Leave;