from payroll.selectors.payroll_selectors import PayrollSelector
from payroll.services.access_service import PayrollAccessService

class PayrollHistoryService:

    @staticmethod
    def get_employee_salary_history(user, path, employee_id=None):

        employee = PayrollAccessService.get_target_employee(user, path, employee_id)

        if not employee:
            return None

        qs = PayrollSelector.get_salary_history(employee)

        return {"rows": qs, "page_obj": qs, "employee": employee}
