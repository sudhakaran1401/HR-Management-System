import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Main/Login";
import LayoutRoute from "./components/LayoutRoute";

import HRDashboard from "./pages/Dashboard/HRDashboard";
import EmployeeDashboard from "./pages/Dashboard/EmployeeDashboard";

import Employees from "./pages/List/Employees";
import Attendance from "./pages/List/Attendance";
import Leaverequest from "./pages/List/Leaverequest";
import Payroll from "./pages/List/Payroll";

import EmployeeReport from "./pages/Report/EmployeeReport";
import AttendanceReport from "./pages/Report/AttendanceReport";
import LeaveReport from "./pages/Report/LeaveReport";
import PayrollReport from "./pages/Report/PayrollReport";

import EmployeeView from "./pages/Views/EmployeeView";
import PayslipView from "./pages/Views/PayslipView";

import EmployeeDelete from "./pages/Form/EmployeeDelete";

import LeaveBalance from "./pages/Dashboard/LeaveBalance";
import AttendanceCalendar from "./pages/Views/AttendanceCalendar";

import EmployeeForm from "./pages/Form/EmployeeForm";
import AttendanceForm from "./pages/Form/AttendanceForm";
import LeaveForm from "./pages/Form/LeaveForm";
import PayrollForm from "./pages/Form/PayrollForm";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public */}
        <Route path="/" element={<Login />} />

        {/* Dashboard */}
        <Route path="/hr/dashboard" element={ <LayoutRoute> <HRDashboard /> </LayoutRoute> } />
        <Route path="/me/dashboard" element={ <LayoutRoute> <EmployeeDashboard /> </LayoutRoute> } />

        {/* Employee */}
        <Route path="/employees" element={ <LayoutRoute> <Employees /> </LayoutRoute> } />
        <Route path="/employees/:id" element={ <LayoutRoute> <EmployeeView /> </LayoutRoute> } />
        <Route path="/me/profile" element={ <LayoutRoute> <EmployeeView /> </LayoutRoute> } />
        <Route path="/employees/delete/:id" element={ <LayoutRoute> <EmployeeDelete /> </LayoutRoute> } />
        <Route path="/employees/create" element={ <LayoutRoute> <EmployeeForm /> </LayoutRoute> } />
        <Route path="/employees/edit/:id" element={ <LayoutRoute> <EmployeeForm /> </LayoutRoute> } />

        {/* Attendance */}
        <Route path="/attendance" element={ <LayoutRoute> <Attendance /> </LayoutRoute> } />
        <Route path="/me/attendance" element={ <LayoutRoute> <Attendance /> </LayoutRoute> } />
        <Route path="/me/attendance-status" element={ <LayoutRoute> <AttendanceCalendar /> </LayoutRoute> } />
        <Route path="/me/mark-attendance" element={ <LayoutRoute> <AttendanceForm /> </LayoutRoute> } />
        <Route path="/employees/mark-attendance" element={ <LayoutRoute> <AttendanceForm /> </LayoutRoute> } />
        <Route path="/employee/:id/mark-attendance" element={ <LayoutRoute> <AttendanceForm /> </LayoutRoute> } />

        {/* Leave */}
        <Route path="/leaverequests" element={ <LayoutRoute> <Leaverequest /> </LayoutRoute> } />
        <Route path="/me/leaverequests" element={ <LayoutRoute> <Leaverequest /> </LayoutRoute> } />
        <Route path="/employee/:employeeId/leaverequests" element={ <LayoutRoute> <Leaverequest /> </LayoutRoute> } />
        <Route path="/leaverequest/create" element={ <LayoutRoute> <LeaveForm /> </LayoutRoute> } />
        <Route path="/leaverequest/edit/:id" element={ <LayoutRoute> <LeaveForm /> </LayoutRoute> } />

        {/* Payroll */}
        <Route path="/payroll" element={ <LayoutRoute> <Payroll /> </LayoutRoute> } />
        <Route path="/me/payroll" element={ <LayoutRoute> <Payroll /> </LayoutRoute> } />
        <Route path="/employee/:employeeId/payroll" element={ <LayoutRoute> <Payroll /> </LayoutRoute> } />
        <Route path="/payroll/payslip/:id" element={ <LayoutRoute> <PayslipView /> </LayoutRoute> } />
        <Route path="/me/payslip/:id" element={ <LayoutRoute> <PayslipView /> </LayoutRoute> } />
        <Route path="/payroll/create" element={ <LayoutRoute> <PayrollForm /> </LayoutRoute> } />
        <Route path="/payroll/edit/:id" element={ <LayoutRoute> <PayrollForm /> </LayoutRoute> } />

        {/* Reports */}
        <Route path="/employees-report" element={ <LayoutRoute> <EmployeeReport /> </LayoutRoute> } />
        <Route path="/attendance-report" element={ <LayoutRoute> <AttendanceReport /> </LayoutRoute> } />
        <Route path="/leave-report" element={ <LayoutRoute> <LeaveReport /> </LayoutRoute> } />
        <Route path="/payroll-report" element={ <LayoutRoute> <PayrollReport /> </LayoutRoute> } />

        {/* Misc */}
        <Route path="/leave-balance" element={ <LayoutRoute> <LeaveBalance /> </LayoutRoute> } />
        <Route path="/employee/:employeeId/leave-balance" element={ <LayoutRoute> <LeaveBalance /> </LayoutRoute> } />

      </Routes>
    </BrowserRouter>
  );
}

export default App;