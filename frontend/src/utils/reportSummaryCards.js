/*
==========================================================
Attendance Summary Cards
==========================================================
*/

export const buildAttendanceSummaryCards = (
  attendanceStats
) => [
  {
    title: "Present",
    value: attendanceStats.present,
    color: "#198754",
  },

  {
    title: "Leave",
    value: attendanceStats.leave,
    color: "#dc3545",
  },

  {
    title: "Holiday",
    value: attendanceStats.holiday,
    color: "#0dcaf0",
  },
];

/*
==========================================================
Leave Summary Cards
==========================================================
*/

export const buildLeaveSummaryCards = (
  leaveStats
) => [
  {
    title: "Applied",
    value: leaveStats.totalApplied,
    color: "#0d6efd",
  },

  {
    title: "Approved",
    value: leaveStats.approved,
    color: "#198754",
  },

  {
    title: "Pending",
    value: leaveStats.pending,
    color: "#ffc107",
  },

  {
    title: "Rejected",
    value: leaveStats.rejected,
    color: "#dc3545",
  },
];