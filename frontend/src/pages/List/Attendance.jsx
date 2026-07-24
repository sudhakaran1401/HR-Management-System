import CrudListPage from "../../components/list/CrudListPage";
import { attendanceColumns } from "../../config/columns/AttendanceColumns";
import { getAttendance } from "../../services/AttendanceService";
import loadEmployeeRecords from "../../utils/loadEmployeeRecords";

import useEmployee from "../../hooks/Employee/useEmployee";

const Attendance = () => {
  const { loggedEmployee } = useEmployee();

  return (
    <CrudListPage
      title="Attendance Records"
      buttonText="+ Mark Attendance"
      searchPlaceholder="Search attendance records..."
      columns={attendanceColumns}
      loadData={({ mergeEmployees }) =>
        loadEmployeeRecords({
          service: getAttendance,
          mergeEmployees,
        })
      }
      filterData={(records, { location }) => {
        if (location.pathname === "/me/attendance") {
          return records.filter(
            (record) =>
              Number(record.employee) ===
              Number(loggedEmployee?.id)
          );
        }

        return records;
      }}
      onButtonClick={({ navigate, location }) =>
        location.pathname === "/me/attendance"
          ? navigate("/me/mark-attendance")
          : navigate("/employees/mark-attendance")
      }
      errorMessage="Unable to load attendance."
    />
  );
};

export default Attendance;