class LeaveStatus:
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class LeaveType:
    SICK = "SICK"
    CASUAL = "CASUAL"
    ANNUAL = "ANNUAL"


class LeaveLimits:
    SICK = 15
    CASUAL = 15
    ANNUAL = 20

class ViewerRole:
    EMPLOYEE = "Employee"
    HR = "HR"


class MessageType:
    SUCCESS = "success"
    ERROR = "error"