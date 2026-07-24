
from leave.constants import LeaveStatus
from leave.models import LeaveRequest
from leave.services.attendance_sync_service import AttendanceSyncService
from django.db import transaction
class ApprovalService:

    @staticmethod
    def update_leave_status( leave, new_status ):

        if leave.status != LeaveStatus.PENDING:

            return ( False, "Only pending leave requests can be updated." )

        leave.status = new_status
        leave.save(update_fields=["status"])
        

        if new_status == LeaveStatus.APPROVED:

            AttendanceSyncService.sync_leave_attendance( leave )

        return True, f"Leave {new_status.lower()} successfully."

    @staticmethod
    def approve_leave(leave):

        with transaction.atomic():

            leave = ( LeaveRequest.objects .select_for_update() .get(id=leave.id) )

        return ApprovalService.update_leave_status( leave, LeaveStatus.APPROVED )


    @staticmethod

    def reject_leave(leave):

        with transaction.atomic():

            leave = ( LeaveRequest.objects .select_for_update() .get(id=leave.id) )

        return ApprovalService.update_leave_status( leave, LeaveStatus.REJECTED )