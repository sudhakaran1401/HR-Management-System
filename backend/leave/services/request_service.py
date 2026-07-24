from leave.validators.leave_validator import LeaveValidator

class RequestService:

    @staticmethod 
    def process_leave_form( form, employee, instance=None ):

        leave = form.save(commit=False)

        is_valid, message = RequestService._validate_leave( employee=employee, leave=leave, exclude_id=( instance.pk if instance else None ) ) 

        if not is_valid:

            return {
                "success": False,
                "message": message
            }

        leave.employee = employee

        leave.save()

        return {
            "success": True,
            "message": (
                "Leave request processed successfully"
            ),
            "data": leave
        }

    @staticmethod
    def _validate_leave( employee, leave, exclude_id=None ):

        validations = [

            LeaveValidator.validate_leave_dates(
                leave.start_date,
                leave.end_date
            ),

            LeaveValidator.check_leave_overlap(
                employee=employee,
                start_date=leave.start_date,
                end_date=leave.end_date,
                exclude_id=exclude_id
            ),

            LeaveValidator.validate_attendance_conflict(
                employee=employee,
                start_date=leave.start_date,
                end_date=leave.end_date
            )
        ]

        for result in validations:

            if not result[0]:
                return False, result[1]

        return True, None

    @staticmethod
    def create_leave( form, employee ):

        return RequestService.process_leave_form( form=form, employee=employee )

    @staticmethod
    def update_leave( form, employee, leave ):

        return RequestService.process_leave_form( form=form, employee=employee, instance=leave )