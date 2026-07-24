from employees.constants import UserGroup


class PermissionService:

    @staticmethod
    def get_user_groups(user):

        return set( user.groups.values_list( "name", flat=True ) )
    
    @staticmethod
    def employee_only(user):

        groups = PermissionService.get_user_groups( user )

        return UserGroup.EMPLOYEE in groups

    @staticmethod
    def hr_or_admin(user):

        if user.is_superuser:
            return True

        groups = PermissionService.get_user_groups( user )

        return bool( { UserGroup.HR, UserGroup.ADMIN } & groups )