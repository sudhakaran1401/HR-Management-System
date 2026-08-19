class DashboardDateFilter:

    @staticmethod
    def apply_filters(qs, field, year=None, month=None, day=None):

        filters = {}

        if year:
            filters[f"{field}__year"] = int(year)

        if month:
            filters[f"{field}__month"] = int(month)

        if day:
            filters[f"{field}__day"] = int(day)

        return qs.filter(**filters)