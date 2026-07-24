/*
==========================================================
Attendance Statistics
==========================================================
*/

export const buildAttendanceStatistics = (
  filteredRecords
) => ({
  present: filteredRecords.filter(
    (row) => row.status === "Present"
  ).length,

  leave: filteredRecords.filter(
    (row) => row.status === "Leave"
  ).length,

  holiday: filteredRecords.filter(
    (row) => row.status === "Holiday"
  ).length,
});

/*
==========================================================
Leave Statistics
==========================================================
*/

export const buildLeaveStatistics = (
  filteredRecords
) => ({
  totalApplied: filteredRecords.length,

  approved: filteredRecords.filter(
    (row) => row.status === "APPROVED"
  ).length,

  pending: filteredRecords.filter(
    (row) => row.status === "PENDING"
  ).length,

  rejected: filteredRecords.filter(
    (row) => row.status === "REJECTED"
  ).length,
});